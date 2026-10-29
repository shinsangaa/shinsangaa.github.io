---
layout: single
title: "날짜별 학습 기록"
permalink: /timeline/
author_profile: true
classes: wide
---

공부한 날짜를 기준으로 **오래된 기록부터** 정리했습니다. 날짜 또는 글 제목을 클릭하면 해당 학습 노트가 열립니다.

<ul style="list-style:none; padding-left:0; margin-left:0;">
{% assign study_days = site.pages | where_exp: "item", "item.study_day" | sort: "study_day" %}
{% for entry in study_days %}
  {% unless entry.study_day == "2026-09-26" %}
    {% assign title_prefix = entry.study_day | append: " · " %}
    {% assign display_title = entry.title | remove_first: title_prefix %}
    <li style="display:flex;flex-wrap:wrap;gap:.3rem 1.1rem;align-items:baseline;padding:.9rem 0;border-bottom:1px solid #e7ebf0;">
      <time style="font-weight:700;min-width:7rem;white-space:nowrap;" datetime="{{ entry.study_day }}">{{ entry.study_day | date: "%Y.%m.%d" }}</time>
      <a style="flex:1;min-width:15rem;" href="{{ entry.url | relative_url }}">{{ display_title | escape }}</a>
    </li>
  {% endunless %}
{% endfor %}
{% assign newest_posts = site.posts | sort: "date" %}
{% for post in newest_posts %}
  {% assign post_day = post.date | date: "%Y%m%d" %}
  {% if post_day >= "20261026" and post.categories contains "class-notes" %}
    {% assign original_date = post.date | date: "%Y-%m-%d" %}
    {% assign post_title_prefix = original_date | append: " | " %}
    {% assign display_title = post.title | remove_first: post_title_prefix %}
    <li style="display:flex;flex-wrap:wrap;gap:.3rem 1.1rem;align-items:baseline;padding:.9rem 0;border-bottom:1px solid #e7ebf0;">
      <time style="font-weight:700;min-width:7rem;white-space:nowrap;" datetime="{{ original_date }}">{{ post.date | date: "%Y.%m.%d" }}</time>
      <a style="flex:1;min-width:15rem;" href="{{ post.url | relative_url }}">{{ display_title | escape }}</a>
    </li>
  {% endif %}
{% endfor %}
</ul>
