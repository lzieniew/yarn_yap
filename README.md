# 100_commitow

# Toolbox for my own use with interesting tools using AI

First plan assumes that I will try doing following tools:
  - Code analysis with local LLM - currently LLMs have limited context size, and because of that when generating code with tools like copilot it tends to create a lot of redundant code, because of lack of ability to search existing codebase for already implemented modules which can be reused. This can be partialy remedied by RAG pipelines, but it's probable that generic RAG solutions doesn't work well with code. I want to test and experiment with other solutions for LLMs to "understand" code.
  - Article to speech - I have a lot of articles and interesting reddit threads that I want to read, but I don't really have time. It would be much easier if I would be able to listen to them. Of course, there are some screen readers etc, but they require user to actively use the computer. My solution will convert article to text and that text to speech, and will upload the audio on youtube or some other hosting service, so it can be listened to in convinient moment.

The first step in all those tools will be to create fast minimal implementation and then test it and experiment with it, so the further decision about what tool I will continue to develop will be made in the future, basing on those informations.

## Article to speech architecture:
  - I will use tortoise tts https://github.com/neonbjb/tortoise-tts for generating voice from text
  - The application will be intended for self hosting, so it will server a single user that has a computer with GPU powerful enough to run voice generation at reasonable speed
  - User will access locally hosted website in order to put there links to articles or reddit threads to convert into speech
  - I will also create API for tortoise TTS, which can be hosted on the same server as the website, or on separate server
  - Website will download user provided websites and will extract text from them. Then it will request Tortoise TTS API for converting this text into speech
  - One of the assumptions is that the server with GPU that will be generating voice doesn't have to online all the time, so the website will have mechanism for checking if the server is available and sending text for generating only when it's online. There will be also an option to see the state of the queue and remove some items from it
  - After generating the voice it will be uploaded to youtube or/and other similar platforms, and added to some predefined playlist. User will be provided with the links by the website and maybe with some other form of notification like email

