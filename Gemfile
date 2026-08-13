source 'https://rubygems.org'

# GitHub Pages (pipeline classica "Deploy from a branch") ignora i pin di
# Jekyll/plugin di questo Gemfile e builda sempre con QUESTA gem, che fissa
# tutte le versioni (Jekyll incluso) a quelle effettivamente in uso in
# produzione. Usarla anche in locale evita che qualcosa funzioni qui e si
# rompa solo alla pubblicazione (jekyll-seo-tag e jekyll-redirect-from sono
# già inclusi come dipendenze di questa gem; la paginazione del blog è
# gestita a mano in _layouts/blog-index.html, non da jekyll-paginate).
gem "github-pages", "~> 232", group: :jekyll_plugins

# Ruby 3.4+ stopped shipping these as default gems; Jekyll/Liquid still need them
gem 'logger'
gem 'bigdecimal'

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem "tzinfo-data"

# Performance-booster for watching directories on Windows
gem "wdm", ">= 0.1.0" if Gem.win_platform?

gem "webrick"
gem "rack", ">= 2.1.4"