---
title: "주제별 공부"
permalink: /topics/
author_profile: true
---

네이버에서 옮긴 **실제 학습 기록을 주제별**로 모았습니다. 한 게시글은 하나의 대표 분야에 배치했으며, 원문 내용과 이미지, 파일명은 그대로 유지했습니다.

{% assign cat = site.categories["python"] | sort: "date" %}
<h2 id="python">Python 기초</h2>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>{{ p.date | date: "%Y.%m.%d" }}</small></li>{% endfor %}</ul>

{% assign cat = site.categories["data-analysis"] | sort: "date" %}
<h2 id="data-analysis">데이터 분석</h2>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>{{ p.date | date: "%Y.%m.%d" }}</small></li>{% endfor %}</ul>

{% assign cat = site.categories["data-visualization"] | sort: "date" %}
<h2 id="data-visualization">데이터 시각화</h2>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>{{ p.date | date: "%Y.%m.%d" }}</small></li>{% endfor %}</ul>

{% assign cat = site.categories["machine-learning"] | sort: "date" %}
<h2 id="machine-learning">머신러닝</h2>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>{{ p.date | date: "%Y.%m.%d" }}</small></li>{% endfor %}</ul>

{% assign cat = site.categories["deep-learning"] | sort: "date" %}
<h2 id="deep-learning">딥러닝</h2>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>{{ p.date | date: "%Y.%m.%d" }}</small></li>{% endfor %}</ul>

{% assign cat = site.categories["llm-agent"] | sort: "date" %}
<h2 id="llm-agent">LLM · AI 에이전트</h2>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>{{ p.date | date: "%Y.%m.%d" }}</small></li>{% endfor %}</ul>

{% assign cat = site.categories["projects"] | sort: "date" %}
<h2 id="projects">프로젝트 · 실습 기획</h2>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>{{ p.date | date: "%Y.%m.%d" }}</small></li>{% endfor %}</ul>

---

### 기타 기록

{% assign cat = site.categories["study-notes"] | sort: "date" %}
<h3 id="study-notes">수업 메모 · 참고 키워드</h3>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>{% endfor %}</ul>

{% assign cat = site.categories["reading"] | sort: "date" %}
<h3 id="reading">뉴스 · 읽을거리</h3>
<ul class="topic-list">{% for p in cat %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>{% endfor %}</ul>
