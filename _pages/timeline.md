---
title: "날짜별 학습 기록"
permalink: /timeline/
author_profile: true
---

**네이버 블로그에서 작성한 학습 기록**을 날짜순으로 모았습니다. 아래 날짜는 현재 Markdown 파일에 저장된 **네이버 게시일** 기준입니다. 실제 수업일과 다를 수 있으며, 수업일이 필요한 글은 본문에 별도로 적어 두었습니다.

{% assign all_posts = site.posts | sort: "date" %}
{% assign previous_day = "" %}
{% for post in all_posts %}
  {% assign current_day = post.date | date: "%Y.%m.%d" %}
  {% if current_day != previous_day %}
### {{ current_day }}
    {% assign previous_day = current_day %}
  {% endif %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
