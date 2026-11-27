---
title: "프로젝트 · 실습 기획"
permalink: /projects/
author_profile: true
---

프로젝트 기획, 구현 과정, 트러블 슈팅, 결과를 모았습니다.

{% assign project_posts = site.categories["projects"] | sort: "date" | reverse %}
{% for post in project_posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) <small>({{ post.date | date: "%Y.%m.%d" }})</small>
{% endfor %}