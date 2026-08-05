package com.algorithmx.datastructure.design;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.TreeMap;

/**
 * 设计 Twitter
 *
 * 核心功能：
 * 1. postTweet(userId, tweetId) — 发推文
 * 2. getNewsFeed(userId) — 获取自己和关注者的最近 10 条推文（时间倒序）
 * 3. follow(followerId, followeeId) — 关注
 * 4. unfollow(followerId, followeeId) — 取关
 *
 * 实现思路：每个用户维护自己的推文链表 + 关注集合，
 * getNewsFeed 时使用多路归并（K 个有序链表合并）获取 Top 10。
 */
class Twitter {
    private static int timestamp = 0;

    static class Tweet {
        int id, time;
        Tweet next;
        Tweet(int id) { this.id = id; this.time = timestamp++; }
    }

    private final Map<Integer, Tweet> tweets;      // userId → 推文链表头
    private final Map<Integer, Set<Integer>> follows; // userId → 关注的人集合

    public Twitter() {
        tweets = new HashMap<>();
        follows = new HashMap<>();
    }

    public void postTweet(int userId, int tweetId) {
        Tweet t = new Tweet(tweetId);
        t.next = tweets.get(userId);
        tweets.put(userId, t);
    }

    /** 获取最近的 10 条推文，包括自己和关注者 */
    public List<Integer> getNewsFeed(int userId) {
        // 多路归并：最大堆按时间戳排序
        PriorityQueue<Tweet> pq = new PriorityQueue<>((a, b) -> b.time - a.time);

        // 自己的推文
        if (tweets.containsKey(userId)) pq.offer(tweets.get(userId));

        // 关注者的推文
        Set<Integer> following = follows.getOrDefault(userId, Collections.emptySet());
        for (int followeeId : following) {
            Tweet t = tweets.get(followeeId);
            if (t != null) pq.offer(t);
        }

        List<Integer> feed = new ArrayList<>();
        for (int i = 0; i < 10 && !pq.isEmpty(); i++) {
            Tweet t = pq.poll();
            feed.add(t.id);
            if (t.next != null) pq.offer(t.next);
        }
        return feed;
    }

    public void follow(int followerId, int followeeId) {
        if (followerId == followeeId) return;
        follows.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);
    }

    public void unfollow(int followerId, int followeeId) {
        Set<Integer> set = follows.get(followerId);
        if (set != null) set.remove(followeeId);
    }
}

/**
 * 设计排行榜 — 支持玩家得分更新和实时排名查询
 *
 * 实现：TreeMap<Score, Set<PlayerId>> + Map<PlayerId, Score>
 * 排行榜按分数降序排列
 */
class Leaderboard {
    private final TreeMap<Integer, Set<Integer>> scoreMap; // score → playerIds（降序用 reverse）
    private final Map<Integer, Integer> playerScore;        // playerId → score

    public Leaderboard() {
        scoreMap = new TreeMap<>(Collections.reverseOrder());
        playerScore = new HashMap<>();
    }

    /** 更新玩家分数（累加或设置） */
    public void addScore(int playerId, int score) {
        Integer oldScore = playerScore.get(playerId);
        if (oldScore != null) {
            Set<Integer> players = scoreMap.get(oldScore);
            players.remove(playerId);
            if (players.isEmpty()) scoreMap.remove(oldScore);
        }
        int newScore = (oldScore == null ? 0 : oldScore) + score;
        playerScore.put(playerId, newScore);
        scoreMap.computeIfAbsent(newScore, k -> new HashSet<>()).add(playerId);
    }

    /** 获取 Top K 分数之和 */
    public int top(int k) {
        int sum = 0;
        for (Map.Entry<Integer, Set<Integer>> entry : scoreMap.entrySet()) {
            int score = entry.getKey();
            int count = entry.getValue().size();
            for (int i = 0; i < count && k > 0; i++, k--) sum += score;
            if (k == 0) break;
        }
        return sum;
    }

    /** 重置玩家分数 */
    public void reset(int playerId) {
        Integer score = playerScore.remove(playerId);
        if (score != null) {
            Set<Integer> players = scoreMap.get(score);
            players.remove(playerId);
            if (players.isEmpty()) scoreMap.remove(score);
        }
    }
}

/**
 * 数据流中位数 — 两个堆实现
 *
 * 维护一个大顶堆（左半部分）和一个小顶堆（右半部分），
 * 使得两个堆大小平衡，中位数由堆顶计算。
 */
class MedianFinder {
    private final PriorityQueue<Integer> left;  // 大顶堆：较小的一半
    private final PriorityQueue<Integer> right; // 小顶堆：较大的一半

    public MedianFinder() {
        left = new PriorityQueue<>(Collections.reverseOrder());
        right = new PriorityQueue<>();
    }

    public void addNum(int num) {
        left.offer(num);
        right.offer(left.poll());
        if (right.size() > left.size()) left.offer(right.poll());
    }

    public double findMedian() {
        if (left.size() > right.size()) return left.peek();
        return (left.peek() + right.peek()) / 2.0;
    }
}

/**
 * 设计循环双端队列（数组实现，无库依赖）
 */
class MyCircularDeque {
    private final int[] arr;
    private int front, rear, size, capacity;

    public MyCircularDeque(int k) {
        capacity = k;
        arr = new int[k];
        front = 0; rear = 0; size = 0;
    }

    public boolean insertFront(int value) {
        if (isFull()) return false;
        front = (front - 1 + capacity) % capacity;
        arr[front] = value;
        size++;
        return true;
    }

    public boolean insertLast(int value) {
        if (isFull()) return false;
        arr[rear] = value;
        rear = (rear + 1) % capacity;
        size++;
        return true;
    }

    public boolean deleteFront() {
        if (isEmpty()) return false;
        front = (front + 1) % capacity;
        size--;
        return true;
    }

    public boolean deleteLast() {
        if (isEmpty()) return false;
        rear = (rear - 1 + capacity) % capacity;
        size--;
        return true;
    }

    public int getFront() { return isEmpty() ? -1 : arr[front]; }
    public int getRear() { return isEmpty() ? -1 : arr[(rear - 1 + capacity) % capacity]; }
    public boolean isEmpty() { return size == 0; }
    public boolean isFull() { return size == capacity; }
    public int size() { return size; }
}
