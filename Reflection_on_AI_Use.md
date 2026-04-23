## 9. Reflection on AI Use

### What Worked Well

Honestly, AI was most useful during the coding phase. Writing Flask routes from scratch is something I find tedious and easy to get wrong — URL patterns, redirects, flash messages, making sure each route reads and writes to the JSON file correctly. When I gave the AI the approved file structure and MVP feature list, it produced clean, readable code that matched what I had designed. I still had to go through it carefully and fix things, but having a working starting point saved a lot of time. The same was true for the tests — I knew what I needed to cover (streak edge cases, duplicate completion prevention, malformed JSON handling) and the AI helped me turn those ideas into actual pytest functions quickly. Beyond coding, it was also useful for structuring report sections — once I gave it a clear persona, constraint list, and output format, the requirements section came together well and I had a proper set of FRs and NFRs to review and adjust rather than starting from nothing.

### What Failed

The early prompts were a mess. My first attempt at generating requirements was something like "generate requirements for a habit tracker app" with no context or constraints. The AI came back with suggestions for user accounts, cloud syncing, and email notifications — none of which were in scope. It also had no memory between sessions, so it would contradict things already agreed, like listing a weekly analytics chart as implemented when I had never approved that. You have to keep feeding it the context it needs, which I did not appreciate at the start.

### How Hallucinations Were Detected and Corrected

Three stood out. First, the analytics chart — the AI pulled it from the general project option description and treated it as if it were in my approved requirements, which it was not. Second, it referred to a test file called "test_habits.py" which did not exist in my project. Third, it described the app as having "robust input sanitisation" when all I had was a basic non-empty name check. I caught all three by reading the output against my actual code and documents rather than accepting it at face value. That habit — treating AI output as a draft to verify, not a source of truth — was the most important thing I took from this project.

### How My Prompting Strategy Changed

I started with short, vague prompts and ended with a structured template reused across every major task. The biggest change was adding a context block at the top of every prompt covering the project constraints, stack, and what not to invent. I also started chaining prompts so each phase built on verified output from the previous one, and got better at specifying the output format, which made responses much easier to use directly in the report.

### What I Learned About AI's Limitations

The main thing is that the AI sounds confident even when it is wrong — which is more dangerous than if it just said it was unsure, because a convincing-sounding paragraph is easy to miss. It also cannot make judgement calls about your specific project scope. It will always fill gaps with something plausible, and plausible is not the same as correct.

### How I Would Improve My Workflow Next Time

I would define the context block and constraints before writing any prompts, rather than working them out after a few bad outputs. I would also run a verifier-style check earlier — after requirements and after design — rather than only before submission.

### Ethical Considerations

The main ethical concern was honesty. Everything the AI produced was reviewed, often corrected, and sometimes rejected outright. The code it helped write still required me to read it, test it, and fix what did not work — so it was a support tool, not a replacement for understanding. Being transparent about where AI contributed and where my own decisions overrode it is what makes the work honest to submit and defensible in a viva. There is also the risk of automation bias, which I fell into early on before I started pushing back on suggestions more consistently. AI is genuinely useful for software development, but that usefulness only holds if the developer stays critical throughout.
