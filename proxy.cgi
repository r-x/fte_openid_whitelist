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
{"accountId":"merchant1","identityType":"merchant","url":"http://merchant1.com","emails":["admin@merchant1.com"],"addresses":[{"street1":"1234 street1","street2":"Suite #250","city":"San Jose","state":"CA","zip":"12345"}],"attributes":[{"name":"displayName","value":["Merchant1"]},{"name":"attribute2","value":["attribute2"]}],"correlationId":"22aa0667df7e6b3d410c612aebbc58b17e90569a","revision":1.0}
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

