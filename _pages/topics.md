---
title: "주제별 공부"
permalink: /topics/
author_profile: true
---

같은 내용을 반복해서 찾기 편하도록 학습 노트를 8개 영역으로 나눴습니다. 각 항목은 작성일 기준으로 **오래된 글부터** 표시합니다.

<h2 id="python">Python 기초</h2>
{% assign subject_posts = site.categories["python"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>

<h2 id="data-analysis">데이터 분석 · Pandas</h2>
{% assign subject_posts = site.categories["data-analysis"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>

<h2 id="data-visualization">데이터 시각화</h2>
{% assign subject_posts = site.categories["data-visualization"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>

<h2 id="machine-learning">머신러닝</h2>
{% assign subject_posts = site.categories["machine-learning"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>

<h2 id="deep-learning">딥러닝</h2>
{% assign subject_posts = site.categories["deep-learning"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>

<h2 id="llm-agent">LLM · AI 에이전트</h2>
{% assign subject_posts = site.categories["llm-agent"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>

<h2 id="projects">프로젝트</h2>
{% assign subject_posts = site.categories["projects"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>

<h2 id="class-notes">수업일지</h2>
{% assign subject_posts = site.categories["class-notes"] | sort: "date" %}
<ul class="topic-list">
{% for post in subject_posts %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y.%m.%d" }})</small></li>{% endfor %}
</ul>
