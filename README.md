# YarnYap - convinient high qualiy articles TTS

A simple tool for automatically converting online articles and Reddit threads into audio files with high quality voice reading them.

<div align="center">
  <img src="docs/logo.png" alt="YarnYap logo" width="40%">
</div>

# What is YarnYap?

It's an easy to deploy web app that makes it easy and convinient to generate high quality voice reading the supplied text, for example articles.
It runs entirely on the user machine, the best results are achieved using the nvidia GPU, but it also supports running on CPU only - it's slower that way, but it can run on practically every hardware.
It's usable even on slower hardware, thanks to built in mechanism of job queue - user can upload a lot of text at once, and it will be automatically processed and available to download after some time. There will be even an option to host main part of the app and voice generating part of the app on separate machines, and the main part of the app will be waiting for generating device to become online

# Features
  - High quality voice generation
  - Convenient UI, allowing user to easily upload text, track the progress and download generated voice files
  - Easy to deploy, just one docker-compose command
  - Queue mechanism, especially useful on slower machines where the generation process can be longer

## Architecture:
  - There will be multiple voice generating agents in use
  - The application will be intended for self hosting, so it will server a single user that has a computer with GPU powerful enough to run voice generation at reasonable speed
  - User will access locally hosted website in order to put there links to articles or reddit threads to convert into speech
  - I will also create API for TTS engine, which can be hosted on the same server as the website, or on separate server
  - Website will download user provided websites and will extract text from them. Then it will request TTS engine API for converting this text into speech
  - One of the assumptions is that the server with GPU that will be generating voice doesn't have to online all the time, so the website will have mechanism for checking if the server is available and sending text for generating only when it's online. There will be also an option to see the state of the queue and remove some items from it
  - After generating the voice it will be uploaded to youtube or/and other similar platforms, and added to some predefined playlist. User will be provided with the links by the website and maybe with some other form of notification like email
  - There will also be a CPU only version of the software, to run on machines without GPU, and standard GPU version. They will differ in the generation container only, to make it consistent

## Architecture diagram

<div align="center">
  <img src="docs/architecture.png" alt="Architecture diagram" width="100%">
</div>
