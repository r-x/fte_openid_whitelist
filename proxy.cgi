#!/usr/bin/ruby

require "cgi"
require "open-uri"
require "net/http"
require "uri"

cgi = CGI.new
puts cgi.header

name = "Rob Corell" # cgi["name"]
url = "foo.com" # cgi["url"]

if name.length == 0
  puts "FAILURE: No name"
elsif url.length == 0 
  puts "FAILURE: No url"
else 
  if( url[0..6] != "http://" )
      url = "http://" + url
  end
  io = open( url )

  if io.status[0] != "200"
    puts "FAILURE: Site not found " + io.status[0]
  else
  
      request_body = %(
        {
            "description" : "Identity Services Profile Create Request",
            "type" : "object",
            "properties" : 
            {
                "identityType" : "merchant",
                "url" : \"#{url}\",
                "attributes" : 
                {
                    "items" : 
                    { 
                       "type" : "object",
                       "properties" : 
                       {
                            "name" : \"#{name}\",
                       }
                    }
                }
            }
        }
      )
    
      puts request_body
      
      whitelist_request_url = URI.parse( "https://identity.arathika.com/idaas/resources/profile" )
      http = Net::HTTP.new( whitelist_request_url.host, 80 )
      request = Net::HTTP::Post.new( whitelist_request_url.request_uri )
      request.body = request_body
      puts whitelist_request_url.request_uri
      response = http.request( request )
      
      puts response
      
  end

end

