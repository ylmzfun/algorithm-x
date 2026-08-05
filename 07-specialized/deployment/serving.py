"""Simple model serving simulation from scratch.

Implements:
- Model loading and prediction serving
- Request/response schema with validation
- Batch inference with configurable batch size
- Mock Flask-style API routing

This is a conceptual simulation; in production you would use
Flask/FastAPI with proper HTTP handling.
"""

from __future__ import annotations

import numpy as np
import json
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime


# ---------------------------------------------------------------------------
# Simple Model for Serving
# ---------------------------------------------------------------------------

class ServingModel:
    """A simple model that can be loaded and served.

    Attributes:
        name: Model name.
        version: Model version string.
        input_dim: Expected input dimension.
        output_dim: Output dimension.
        weights: Model weight matrices.
    """

    def __init__(
        self,
        name: str = "default_model",
        version: str = "1.0.0",
        input_dim: int = 10,
        output_dim: int = 3,
        seed: int = 42,
    ) -> None:
        """Initialize the model.

        Args:
            name: Model identifier.
            version: Semantic version string.
            input_dim: Input dimension.
            output_dim: Output dimension.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.name = name
        self.version = version
        self.input_dim = input_dim
        self.output_dim = output_dim

        # Simple two-layer weights
        hidden = 16
        self.W1: np.ndarray = rng.normal(0, 0.5, (input_dim, hidden))
        self.b1: np.ndarray = np.zeros(hidden)
        self.W2: np.ndarray = rng.normal(0, 0.5, (hidden, output_dim))
        self.b2: np.ndarray = np.zeros(output_dim)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Run inference.

        Args:
            x: Input [B, input_dim] or [input_dim].

        Returns:
            Class probabilities [B, output_dim] or [output_dim].
        """
        if x.ndim == 1:
            x = x.reshape(1, -1)

        h = np.maximum(0, x @ self.W1 + self.b1)
        logits = h @ self.W2 + self.b2
        probs = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probs = probs / np.sum(probs, axis=-1, keepdims=True)
        return probs.squeeze() if x.shape[0] == 1 else probs


# ---------------------------------------------------------------------------
# Request/Response Schema
# ---------------------------------------------------------------------------

@dataclass
class PredictionRequest:
    """Schema for a single prediction request.

    Attributes:
        id: Unique request identifier.
        features: Input feature vector as list of floats.
        model_name: Optional model selection.
        timestamp: Request creation time.
    """
    id: str
    features: list[float]
    model_name: str = "default_model"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def validate(self) -> tuple[bool, str]:
        """Validate the request data.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if not self.id:
            return False, "Request ID is required"
        if not self.features:
            return False, "Features cannot be empty"
        if not all(isinstance(f, (int, float)) for f in self.features):
            return False, "All features must be numeric"
        return True, ""

    def to_array(self) -> np.ndarray:
        """Convert features to numpy array.

        Returns:
            Feature vector [n_features].
        """
        return np.array(self.features, dtype=np.float64)


@dataclass
class PredictionResponse:
    """Schema for a prediction response.

    Attributes:
        request_id: Matching request identifier.
        predictions: Predicted class probabilities as list.
        predicted_class: Index of the most probable class.
        confidence: Confidence score of the predicted class.
        model_name: Model that served the request.
        model_version: Model version.
        processing_time_ms: Inference time in milliseconds.
    """
    request_id: str
    predictions: list[float]
    predicted_class: int
    confidence: float
    model_name: str
    model_version: str
    processing_time_ms: float = 0.0


@dataclass
class BatchPredictionRequest:
    """Schema for batch prediction requests.

    Attributes:
        requests: List of individual prediction requests.
    """
    requests: list[PredictionRequest]

    def validate(self) -> tuple[bool, str]:
        """Validate all requests in the batch.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if not self.requests:
            return False, "Batch cannot be empty"
        for i, req in enumerate(self.requests):
            ok, err = req.validate()
            if not ok:
                return False, f"Request[{i}]: {err}"
        return True, ""


# ---------------------------------------------------------------------------
# Model Server
# ---------------------------------------------------------------------------

class ModelServer:
    """Simple model server that handles prediction requests.

    Manages model loading and request processing.

    Attributes:
        model: The loaded serving model.
    """

    def __init__(self, model: ServingModel) -> None:
        """Initialize the server with a model.

        Args:
            model: The model to serve.
        """
        self.model = model

    def predict_single(self, request: PredictionRequest) -> PredictionResponse:
        """Process a single prediction request.

        Args:
            request: Validated prediction request.

        Returns:
            Prediction response.
        """
        t_start = datetime.now()
        features = request.to_array()
        probs = self.model.predict(features)
        pred_class = int(np.argmax(probs))
        confidence = float(probs[pred_class])
        elapsed = (datetime.now() - t_start).total_seconds() * 1000

        return PredictionResponse(
            request_id=request.id,
            predictions=probs.tolist(),
            predicted_class=pred_class,
            confidence=confidence,
            model_name=self.model.name,
            model_version=self.model.version,
            processing_time_ms=elapsed,
        )

    def handle_request(self, raw_request: dict) -> PredictionResponse:
        """Full request handling with validation.

        Args:
            raw_request: Dictionary with 'id' and 'features' keys.

        Returns:
            Prediction response or error indicator.

        Raises:
            ValueError: If the request is invalid.
        """
        # Build request object
        req = PredictionRequest(
            id=raw_request.get("id", ""),
            features=raw_request.get("features", []),
            model_name=raw_request.get("model_name", "default_model"),
        )

        # Validate
        ok, err = req.validate()
        if not ok:
            raise ValueError(f"Invalid request: {err}")

        # Check model name
        if req.model_name != self.model.name:
            raise ValueError(
                f"Model '{req.model_name}' not found. "
                f"Available: '{self.model.name}'"
            )

        return self.predict_single(req)


# ---------------------------------------------------------------------------
# Batch Predictor
# ---------------------------------------------------------------------------

class BatchPredictor:
    """Handles batch inference with configurable batch size.

    Attributes:
        server: The model server.
        max_batch_size: Maximum number of requests to process at once.
    """

    def __init__(self, server: ModelServer, max_batch_size: int = 32) -> None:
        """Initialize the batch predictor.

        Args:
            server: Model server instance.
            max_batch_size: Maximum batch size.
        """
        self.server = server
        self.max_batch_size = max_batch_size

    def predict_batch(
        self, batch_request: BatchPredictionRequest
    ) -> list[PredictionResponse]:
        """Process a batch of requests.

        Args:
            batch_request: Batch prediction request.

        Returns:
            List of prediction responses.
        """
        ok, err = batch_request.validate()
        if not ok:
            raise ValueError(f"Invalid batch: {err}")

        responses: list[PredictionResponse] = []
        for req in batch_request.requests:
            try:
                resp = self.server.predict_single(req)
                responses.append(resp)
            except Exception as e:
                # In production, log the error and continue
                responses.append(PredictionResponse(
                    request_id=req.id,
                    predictions=[],
                    predicted_class=-1,
                    confidence=0.0,
                    model_name=self.server.model.name,
                    model_version=self.server.model.version,
                ))

        return responses

    def predict_batch_efficient(
        self, batch_request: BatchPredictionRequest
    ) -> list[PredictionResponse]:
        """Process a batch by stacking requests into a single tensor.

        More efficient than individual predictions.

        Args:
            batch_request: Batch prediction request.

        Returns:
            List of prediction responses.
        """
        ok, err = batch_request.validate()
        if not ok:
            raise ValueError(f"Invalid batch: {err}")

        # Stack all features
        all_features = np.stack(
            [req.to_array() for req in batch_request.requests]
        )
        all_probs = self.server.model.predict(all_features)

        responses: list[PredictionResponse] = []
        for i, req in enumerate(batch_request.requests):
            probs = all_probs[i]
            pred_class = int(np.argmax(probs))
            confidence = float(probs[pred_class])
            responses.append(PredictionResponse(
                request_id=req.id,
                predictions=probs.tolist(),
                predicted_class=pred_class,
                confidence=confidence,
                model_name=self.server.model.name,
                model_version=self.server.model.version,
            ))
        return responses


# ---------------------------------------------------------------------------
# Flask-like API simulation
# ---------------------------------------------------------------------------

class MockFlaskAPI:
    """Simulated Flask API for model serving.

    Defines route handlers and provides a simulate_request method
    for testing without running an actual HTTP server.

    Attributes:
        model: The served model.
        server: The ModelServer.
        batch_predictor: The BatchPredictor.
    """

    def __init__(
        self, model: ServingModel, max_batch_size: int = 32
    ) -> None:
        """Initialize the mock API.

        Args:
            model: Model to serve.
            max_batch_size: Maximum batch size.
        """
        self.model = model
        self.server = ModelServer(model)
        self.batch_predictor = BatchPredictor(self.server, max_batch_size)

    def route_predict(self, request_data: dict) -> PredictionResponse:
        """POST /predict — single prediction endpoint.

        Args:
            request_data: Request body with 'id' and 'features'.

        Returns:
            Prediction response.
        """
        return self.server.handle_request(request_data)

    def route_batch_predict(self, request_data: dict) -> list[PredictionResponse]:
        """POST /batch_predict — batch prediction endpoint.

        Args:
            request_data: Request body with 'requests' list.

        Returns:
            List of prediction responses.
        """
        reqs = [
            PredictionRequest(
                id=r["id"],
                features=r["features"],
                model_name=r.get("model_name", "default_model"),
            )
            for r in request_data["requests"]
        ]
        batch = BatchPredictionRequest(requests=reqs)
        return self.batch_predictor.predict_batch_efficient(batch)

    def route_health(self) -> dict:
        """GET /health — health check endpoint.

        Returns:
            Health status dictionary.
        """
        return {
            "status": "healthy",
            "model_name": self.model.name,
            "model_version": self.model.version,
            "input_dim": self.model.input_dim,
            "output_dim": self.model.output_dim,
        }

    def simulate_request(
        self, endpoint: str, data: dict
    ) -> dict | list[dict]:
        """Simulate an HTTP request to a given endpoint.

        Args:
            endpoint: Route name: 'predict', 'batch_predict', or 'health'.
            data: Request body.

        Returns:
            Response body (dict or list of dicts).
        """
        if endpoint == "predict":
            resp = self.route_predict(data)
            return {
                "request_id": resp.request_id,
                "predictions": resp.predictions,
                "predicted_class": resp.predicted_class,
                "confidence": resp.confidence,
                "model_name": resp.model_name,
                "model_version": resp.model_version,
            }
        elif endpoint == "batch_predict":
            resps = self.route_batch_predict(data)
            return [
                {
                    "request_id": r.request_id,
                    "predictions": r.predictions,
                    "predicted_class": r.predicted_class,
                    "confidence": r.confidence,
                }
                for r in resps
            ]
        elif endpoint == "health":
            return self.route_health()
        else:
            return {"error": f"Unknown endpoint: {endpoint}"}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing serving.py — Model Serving")
    print("=" * 60)

    all_pass = True

    # Create model and API
    model = ServingModel(
        name="classifier_v1",
        version="1.0.0",
        input_dim=10,
        output_dim=3,
        seed=42,
    )
    api = MockFlaskAPI(model)

    # Test 1: Health check
    print("\n--- Health Check ---")
    health = api.simulate_request("health", {})
    print(f"  Status: {health['status']}")
    print(f"  Model: {health['model_name']} v{health['model_version']}")
    health_ok = health["status"] == "healthy"
    all_pass = all_pass and health_ok

    # Test 2: Single prediction
    print("\n--- Single Prediction ---")
    req_data = {
        "id": "req-001",
        "model_name": "classifier_v1",
        "features": [0.5, -0.3, 0.1, 0.8, -0.2, 0.6, -0.1, 0.4, -0.5, 0.9],
    }
    resp = api.simulate_request("predict", req_data)
    print(f"  Request ID: {resp['request_id']}")
    print(f"  Predicted class: {resp['predicted_class']}")
    print(f"  Confidence: {resp['confidence']:.3f}")
    print(f"  Probabilities: {[f'{p:.3f}' for p in resp['predictions']]}")

    # Verify probabilities sum to 1
    probs_sum = abs(sum(resp["predictions"]) - 1.0) < 0.01
    print(f"  Probabilities sum to 1: {probs_sum}")
    all_pass = all_pass and probs_sum

    # Test 3: Batch prediction
    print("\n--- Batch Prediction ---")
    batch_data = {
        "requests": [
            {"id": "batch-001", "model_name": "classifier_v1", "features": [float(i % 10) * 0.1 for i in range(10)]},
            {"id": "batch-002", "model_name": "classifier_v1", "features": [(float(i % 10) - 5) * 0.2 for i in range(10)]},
            {"id": "batch-003", "model_name": "classifier_v1", "features": [0.0] * 10},
        ]
    }
    batch_resp = api.simulate_request("batch_predict", batch_data)
    print(f"  Batch responses: {len(batch_resp)}")
    for r in batch_resp:
        print(f"    {r['request_id']}: class={r['predicted_class']}, "
              f"conf={r['confidence']:.3f}")
    batch_ok = len(batch_resp) == 3
    all_pass = all_pass and batch_ok

    # Test 4: Request validation
    print("\n--- Request Validation ---")
    # Invalid: empty features
    try:
        api.simulate_request("predict", {"id": "bad-req", "features": []})
        print("  Empty features: should have raised ValueError")
        all_pass = False
    except ValueError as e:
        print(f"  Empty features rejected: {e}")

    # Invalid: wrong model name
    try:
        api.simulate_request("predict", {
            "id": "bad-model",
            "features": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            "model_name": "nonexistent_model",
        })
        print("  Wrong model: should have raised ValueError")
        all_pass = False
    except ValueError as e:
        print(f"  Wrong model rejected: {e}")

    # Test 5: Schema objects
    print("\n--- Schema Objects ---")
    req = PredictionRequest(id="test", features=[1.0, 2.0, 3.0])
    ok, err = req.validate()
    print(f"  Valid request: {ok}")
    all_pass = all_pass and ok

    # Test 6: Efficient batch prediction
    print("\n--- Efficient Batch ---")
    batch_req = BatchPredictionRequest(requests=[
        PredictionRequest(id=f"eff-{i}", features=[float(j) * 0.1 for j in range(10)])
        for i in range(5)
    ])
    eff_resp = api.batch_predictor.predict_batch_efficient(batch_req)
    print(f"  Efficient batch responses: {len(eff_resp)}")
    eff_ok = len(eff_resp) == 5
    all_pass = all_pass and eff_ok

    print(f"\n{'PASS' if all_pass else 'FAIL'}: serving.py")
