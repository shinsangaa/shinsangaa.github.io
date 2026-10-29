---
title: "프로젝트 · 실습 기획"
permalink: /projects/
author_profile: true
---

공부하면서 작성한 **실습 과제와 프로젝트 기획 메모**를 모았습니다.

{% assign project_posts = site.categories["projects"] | sort: "date" | reverse %}
{% for post in project_posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) <small>({{ post.date | date: "%Y.%m.%d" }})</small>
{% endfor %}

앞으로 실제 구현한 프로젝트의 개발 과정, 결과, 회고를 이곳에 추가할 수 있습니다.
