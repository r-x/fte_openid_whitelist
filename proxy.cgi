#!/usr/bin/ruby

require "cgi"
require "open-uri"
require "net/https"
require "uri"

cgi = CGI.new
puts cgi.header

begin
	url 	= cgi.params["url"][0]
	name 	= cgi.params["name"][0]
	
	if name.length == 0
		puts "FAILURE: No name"
	elsif url.length == 0 
		puts "FAILURE: No url"
	else 
		if( url[0..6] != "http://" )
			url = "http://" + url
		end
		
		begin 
			io = open( url )
			urlFound = io.status[0] == "200"
		rescue Exception => e
			urlFound = false;
		end
	
		if !urlFound
			puts "FAILURE: Site not found"
    else
			request_body = %({\"identityType\":\"merchant\",\"url\":\"#{url}\",\"attributes\":[{\"name\":\"#{name}\"}]}")
			whitelist_request_url = URI.parse( "https://identity.arathika.com/idaas/resources/profile" )
			http = Net::HTTP.new( whitelist_request_url.host, 443 )
			request = Net::HTTP::Post.new( whitelist_request_url.request_uri, { "User-Agent" => "Ruby/#{RUBY_VERSION}" }  )
			http.use_ssl = true
			request.content_type = "application/json"
			request.body = request_body
			response = http.request( request )
			  
			if( response.body.index("\"statusMessage\":\"SUCCESS\"") != nil )
				puts "SUCCESS"
			else
				puts "FAILURE:" + response.body
			end
		end
	end
rescue Exception => e
	puts "FAILURE: Script exception: " + e.message
end
