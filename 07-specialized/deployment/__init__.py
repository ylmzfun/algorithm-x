"""Model Deployment module.

Implementations of deployment-related concepts from scratch using NumPy:
- Model Export (NumPy serialization, JSON)
- Quantization (symmetric/asymmetric, simulated 8-bit)
- Knowledge Distillation (teacher-student, soft targets)
- Model Serving (Flask-like API, batch inference)
"""

__all__ = ["model_export", "quantization", "knowledge_distillation", "serving"]
