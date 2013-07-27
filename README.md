Server-side Video Editing
=========
Sample scripts for the [Kitchen Table Coders](http://kitchentablecoders.com/2013/07/27/server-side-video/) workshop of the same name.

##Why?

While there have been some great projects that use browser-based real-time graphics teqhniques combined with video sharing APIs to create interactive, video-driven experiences, the results of these types of projects are usually fleeting. What if you want to allow users to create a custom, shareable, downloadable video artifact that draws from the huge world of source audio and video out there on the web? In this workshop, we will explore a suite of tools that can be used to create a server-side video editing platform that can churn out customized video files based on logic that we provide. I like to call this process “procedural video editing”, and while it’s nowhere near as sophisticated as a tool like FinalCut, it is very powerful nonetheless.


### What?
This repo contains a set of Python scripts that illustrate a bunch of techniques that I found helpful in the 2 or 3 projects where I've used server-side editing: a process that I've found to be sorely under-documented. They are meant to be looked at sequentially. Generally, the process goes like this:

* short introduction to using Python as a shell-scripting tool
* gathering source material using various tools
* ffmpeg 
	* for conversion
	* for video information
	* for video layout
* introduction to MLT
* turning Google API stuff into videos

## Colophon

* [youtube-dl](http://rg3.github.io/youtube-dl/)
	* [Youtube Feeds api](https://developers.google.com/youtube/2.0/developers_guide_protocol_video_feeds)
* [python](http://www.python.org/)
	* [Python Imaging Library](http://www.pythonware.com/products/pil/)
	* [Mutagen](https://code.google.com/p/mutagen/)
	* [Requests](http://docs.python-requests.org/en/latest/)
* [ffmpeg](http://www.ffmpeg.org/)
* [MLT](http://www.mltframework.org/) (mlt) 
	* [Frei0r plugins](http://frei0r.dyne.org/)
* [Echonest API](http://developer.echonest.com/docs/v4/)
* Google APIs
	* [Directions](https://developers.google.com/maps/documentation/directions/)
	* [Street View](https://developers.google.com/maps/documentation/streetview/)
