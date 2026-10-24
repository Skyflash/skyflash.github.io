# Genera le pagine 2..N della paginazione del blog, una serie per lingua.
#
# La paginazione la fa _layouts/blog-index.html (filtra i post per lingua,
# cosa che jekyll-paginate non sa fare), ma ogni pagina prima doveva esistere
# come file scritto a mano (it/blog/pagina2.html, pagina3.html...): quando i
# post superavano un multiplo di blog_posts_per_page il link "Più vecchi"
# finiva in 404. Qui si parte dalle pagine indice (layout blog-index, senza
# page_num o con page_num 1) e si clonano quante pagine servono, con lo
# stesso conteggio del layout: post della lingua, meno quello in vetrina.
#
# Priorità :high per girare prima di jekyll-redirect-from, che così vede il
# redirect_from delle pagine generate.
module BlogPagination
  class Generator < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      per_page = site.config["blog_posts_per_page"].to_i
      return if per_page <= 0

      indexes = site.pages.select do |page|
        page.data["layout"] == "blog-index" && page.data.fetch("page_num", 1).to_i == 1
      end

      indexes.each do |index|
        lang_posts = site.posts.docs.select { |post| post.data["lang"] == index.data["lang"] }
        grid_size = lang_posts.size - (lang_posts.any? { |post| post.data["featured"] } ? 1 : 0)
        total_pages = (grid_size + per_page - 1) / per_page

        (2..total_pages).each { |num| site.pages << build_page(site, index, num) }
      end
    end

    private

    def build_page(site, index, num)
      dir = index.url.sub(%r{index\.html\z}, "")
      page = Jekyll::PageWithoutAFile.new(site, site.source, dir, "pagina#{num}/index.html")
      page.data = index.data.merge(
        "page_num" => num,
        "permalink" => "#{dir}pagina#{num}/"
      )
      redirect = index.data["redirect_from"]
      page.data["redirect_from"] = "#{redirect}pagina#{num}/" if redirect.is_a?(String)
      page.content = index.content
      page
    end
  end
end
