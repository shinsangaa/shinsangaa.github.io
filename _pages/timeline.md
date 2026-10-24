---
title: "날짜별 학습 기록"
permalink: /timeline/
author_profile: true
---

수업일을 기준으로 **오래된 날짜부터** 정리했습니다. 카페 게시글의 작성일과 수업일이 다르면 게시글 제목 속 수업일을 우선했습니다.

{% assign logs = site.posts | where: "series", "수업일지" | sort: "date" %}
{% for post in logs %}
### {{ post.date | date: "%Y.%m.%d" }} · [{{ post.title }}]({{ post.url | relative_url }})
{{ post.excerpt | strip_html | strip_newlines | truncate: 145 }}
{% endfor %}

---
[주제별 개념 정리 바로가기]({{ '/topics/' | relative_url }})
