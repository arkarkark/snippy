# Find the JRuby version from .ruby-version to keep compatibility
# with tools that exclusively use .ruby-version.
RUBY_VERSION = File.read(File.join(File.dirname(__FILE__), '.ruby-version')).split('-').last.chomp

ruby '2.1.3', engine: 'ruby', engine_version: RUBY_VERSION

source "https://rubygems.org"

group :development, :test do
  gem 'slim',             '2.0.1'
end
