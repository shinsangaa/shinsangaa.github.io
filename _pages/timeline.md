---
layout: single
title: "날짜별 학습 기록"
permalink: /timeline/
author_profile: true
classes: wide
---

공부한 날짜를 기준으로 정리했습니다. 날짜 또는 글 제목을 클릭하면 해당 학습 노트가 열립니다.

<ul style="list-style:none; padding-left:0; margin-left:0;">
{% assign dated_posts = site.posts | where_exp: "item", "item.course_date" | sort: "course_date" %}
{% for post in dated_posts %}
  {% unless post.categories contains "projects" %}
    {% assign title_prefix = post.course_date | append: " | " %}
    {% assign display_title = post.title | remove_first: title_prefix %}
    <li style="display:flex;flex-wrap:wrap;gap:.3rem 1.1rem;align-items:baseline;padding:.9rem 0;border-bottom:1px solid #e7ebf0;">
      <time style="font-weight:700;min-width:7rem;white-space:nowrap;" datetime="{{ post.course_date }}">{{ post.course_date | date: "%Y.%m.%d" }}</time>
      <a style="flex:1;min-width:15rem;" href="{{ post.url | relative_url }}">{{ display_title | escape }}</a>
    </li>
  {% endunless %}
{% endfor %}
</ul>