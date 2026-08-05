package com.algorithmx.datastructure.design;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

class DesignProblemsTest {

    @Test void twitter() {
        Twitter twitter = new Twitter();
        twitter.postTweet(1, 5);
        assertEquals(List.of(5), twitter.getNewsFeed(1));

        twitter.follow(1, 2);
        twitter.postTweet(2, 6);
        assertEquals(List.of(6, 5), twitter.getNewsFeed(1));

        twitter.unfollow(1, 2);
        assertEquals(List.of(5), twitter.getNewsFeed(1));
    }

    @Test void twitterMultiFeed() {
        Twitter twitter = new Twitter();
        twitter.postTweet(1, 1);
        twitter.postTweet(1, 2);
        twitter.follow(1, 2);
        twitter.postTweet(2, 3);
        twitter.postTweet(2, 4);
        List<Integer> feed = twitter.getNewsFeed(1);
        assertEquals(List.of(4, 3, 2, 1), feed);
    }

    @Test void leaderboard() {
        Leaderboard lb = new Leaderboard();
        lb.addScore(1, 73);
        lb.addScore(2, 56);
        lb.addScore(3, 39);
        lb.addScore(4, 51);
        lb.addScore(5, 4);
        assertEquals(73, lb.top(1));
        assertEquals(73 + 56, lb.top(2));

        lb.reset(1);
        lb.reset(2);
        lb.addScore(2, 51);
        assertEquals(51 + 51, lb.top(2)); // player 2=51, player 4=51
    }

    @Test void medianFinder() {
        MedianFinder mf = new MedianFinder();
        mf.addNum(1);
        assertEquals(1.0, mf.findMedian(), 0.001);
        mf.addNum(2);
        assertEquals(1.5, mf.findMedian(), 0.001);
        mf.addNum(3);
        assertEquals(2.0, mf.findMedian(), 0.001);
    }

    @Test void circularDeque() {
        MyCircularDeque dq = new MyCircularDeque(3);
        assertTrue(dq.insertLast(1));
        assertTrue(dq.insertLast(2));
        assertTrue(dq.insertFront(3));
        assertFalse(dq.insertFront(4)); // full
        assertEquals(2, dq.getRear());
        assertTrue(dq.isFull());
        assertTrue(dq.deleteLast());
        assertTrue(dq.insertFront(4));
        assertEquals(4, dq.getFront());
    }
}
