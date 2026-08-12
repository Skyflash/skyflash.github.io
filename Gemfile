source 'https://rubygems.org'

gem 'jekyll', '~> 4.4'

# Ruby 3.4+ stopped shipping these as default gems; Jekyll/Liquid still need them
gem 'logger'
gem 'bigdecimal'

group :jekyll_plugins do
    gem 'jekyll-seo-tag'
    gem 'jekyll-redirect-from'
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem "tzinfo-data"

# Performance-booster for watching directories on Windows
gem "wdm", ">= 0.1.0" if Gem.win_platform?

gem "webrick"
gem "rack", ">= 2.1.4"