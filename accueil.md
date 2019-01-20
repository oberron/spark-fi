---
layout: default
ref: index
lang: fr
---

<div id="home">
  <h1>{{ site.title }}</h1>
  <hr />

  <ol class="posts">
    {% for post in paginator.posts %}
      <li><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a> &raquo; <i><span>{{ post.date | date_to_string }}</span></i></li>
    {% endfor %}
  </ol>

  <!-- Pagination links -->
  {% if paginator.total_pages > 1 %}
    <ul class="pagination pagination-sm">
      {% if paginator.previous_page %}
        <li><a href="{{ paginator.previous_page_path | prepend: site.baseurl | replace: '//', '/' }}">&laquo;</a></li>
      {% else %}
        <li class="disabled"><span aria-hidden="true">&laquo;</span></li>
      {% endif %}

      <li><a href="{{site.baseurl}}/">First</a></li>

      {% for page in (1..paginator.total_pages) %}
        {% if page == paginator.page %}
          <li class="active"><a>{{ page }}<span class="sr-only">(current)</span></a></li>
        {% elsif page == 1 %}
          <li><a href="{{site.baseurl}}/">{{ page }}</a></li>
        {% else %}
          <li><a href="{{ site.paginate_path | prepend: site.baseurl | replace: '//', '/' | replace: ':num', page }}">{{ page }}</a></li>
        {% endif %}
      {% endfor %}

      <li><a href="{{site.baseurl}}/page/{{ paginator.total_pages }}/">Last</a></li>

      {% if paginator.next_page %}
        <li><a href="{{ paginator.next_page_path | prepend: site.baseurl | replace: '//', '/' }}">&raquo;</a></li>
      {% else %}
        <li class="disabled"><span>&raquo;</span></li>
      {% endif %}
    </ul>
  {% endif %}
</div><!-- end #home -->