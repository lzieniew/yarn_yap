# 100_commitow

Toolbox for my own use with interesting tools using AI

First plan assumes that I will try doing following tools:
  - Code analysis with local LLM - currently LLMs have limited context size, and because of that when generating code with tools like copilot it tends to create a lot of redundant code, because of lack of ability to search existing codebase for already implemented modules which can be reused. This can be partialy remedied by RAG pipelines, but it's probable that generic RAG solutions doesn't work well with code. I want to test and experiment with other solutions for LLMs to "understand" code.
  - Article to speech - I have a lot of articles and interesting reddit threads that I want to read, but I don't really have time. It would be much easier if I would be able to listen to them. Of course, there are some screen readers etc, but they require user to actively use the computer. My solution will convert article to text and that text to speech, and will upload the audio on youtube or some other hosting service, so it can be listened to in convinient moment.

The first step in all those tools will be to create fast minimal implementation and then test it and experiment with it, so the further decision about what tool I will continue to develop will be made in the future, basing on those informations.
