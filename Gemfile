# frozen_string_literal: true

source 'https://rubygems.org'

ruby '>= 2.7.0'

# 开发依赖
group :development do
  gem 'rubocop', '~> 1.50'
  gem 'rubocop-performance', '~> 1.16'
  gem 'yard', '~> 0.9'
end

# 测试依赖
group :test do
  gem 'minitest', '~> 5.18'
  gem 'benchmark-ips', '~> 2.10'
end

# 可选的性能分析工具
group :development, :test do
  gem 'memory_profiler', '~> 1.0'
  gem 'ruby-prof', '~> 1.6'
end