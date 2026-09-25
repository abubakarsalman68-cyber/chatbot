# Python for Applied AI — Day 1

## Lab and homework worksheet

**Your first notebook, your first errors, your first useful script**

| | |
|---|---|
| Name | |
| Trade | AI for Everyone — Python track |
| Session / batch | |
| Date | |

> **The rule for this track:** type it yourself first, ask the assistant second. Everything on this sheet is typed by hand. No pasting today.

---

## What you hand in next session

1. A Colab notebook saved in your own Drive, with both labs in it.
2. Three errors you caused on purpose, with what each one told you.
3. Your own version of the name-cleaning script.
4. A messy list from your real work, ready for next session.

**Time needed:** 65 minutes in class, about 20 minutes at home.

---

## Part A · Setup — five minutes

- [ ] Opened **colab.research.google.com**
- [ ] Signed in with the Google account from Week 1
- [ ] Clicked **New notebook**
- [ ] Renamed it: `Python Day 1 — [your name]`
- [ ] Found it in Drive, under the folder **Colab Notebooks**

**If something failed, write what happened:**

_______________________________________________________________________

> Nothing is installed on your computer. If the power goes, your notebook is safe in Drive — you lose the last few minutes, not the work.

---

## Part B · Lab 1 — your first notebook

Type each block into a **separate cell**. Press **Shift + Enter** to run a cell.

### Cell 1

```python
name = "Bilal"
city = "Lahore"
print("Hey,", name, "from", city)
```

**What did it print?**

_______________________________________________________________________

### Cell 2

```python
orders = [120, 340, 90, 560]
print("Total:", sum(orders))
print("Biggest:", max(orders))
```

**What did it print?**

_______________________________________________________________________

### Cell 3 — make it yours

Change the name, the city and the numbers to your own. Run it again.

**Your version printed:**

_______________________________________________________________________

### Name what you just used

| Word | What it means, in your own words |
|---|---|
| Variable (`name`, `city`) | |
| List (`orders`) | |
| Function (`print`, `sum`, `max`) | |

---

## Part C · Break it on purpose

This is the most important twenty minutes of the day. Cause each error deliberately.

**How to read an error:** the **last line** names the problem. The lines above it are the path Python took to get there.

| # | What you changed | The last line of the error | What it meant, in your words | How you fixed it |
|---|---|---|---|---|
| 1 | Deleted a quotation mark | | | |
| 2 | Misspelled a variable name | | | |
| 3 | `print("Total: " + 120)` | | | |

**Which error was hardest to understand, and why?**

_______________________________________________________________________

> An error is Python telling you exactly where it got confused. It is information, not rejection.

---

## Part D · Lab 2 — something actually useful

Type this into a new cell:

```python
names = ["  ali khan ", "SARA AHMED", "bilal  ", " Ayesha Khan"]

for raw in names:
    clean = raw.strip().title()
    print(clean)
```

> **Watch the indentation.** The two lines under `for` must be pushed in. Colab does it for you when you press Enter after the colon — do not fight it.

**What did it print?**

_______________________________________________________________________

### Now change things and see what happens

| Change | What happened |
|---|---|
| Replace `.title()` with `.upper()` | |
| Remove `.strip()` | |
| Add your own messy name to the list | |
| Remove the indentation on the last line | |

**In one sentence — what does `.strip()` do?**

_______________________________________________________________________

**In one sentence — what does the `for` line do?**

_______________________________________________________________________

---

## Part E · How to ask the assistant — pass two

You may ask for help **after** you have attempted it. Ask for an explanation, not for code.

**Use this shape:**

> I am learning Python. Here is my code: [paste your code]
> Here is the error: [paste the whole error]
> Explain why this happened in simple English. **Do not rewrite my code** — tell me what to change and I will type it.

**One question you asked today, and what you learned from the answer:**

_______________________________________________________________________

_______________________________________________________________________

---

## Part F · Homework — twenty minutes, not two hours

1. **Retype both labs** from scratch in a new notebook, without looking at this sheet. Note where you got stuck.
2. **Cause three more errors** — different ones from Part C — and write down what each said.
3. **Bring a messy list**: real names, products, cities or items from your work, your family's business, or your phone contacts.

**Where I got stuck when retyping:**

_______________________________________________________________________

**The messy list I am bringing:**

_______________________________________________________________________

---

## Before you submit

- [ ] Name, trade and session at the top
- [ ] Notebook saved in Drive with your name in the title
- [ ] Both labs typed by hand — nothing pasted
- [ ] Output written down for each cell
- [ ] Three deliberate errors recorded with their last lines
- [ ] Four changes tried in Lab 2, with what happened
- [ ] `.strip()` and `for` explained in your own words
- [ ] A messy list ready for next session

---

## For the trainer

**What good work looks like**

- The error table is filled with the **actual last line**, copied exactly — `SyntaxError: unterminated string literal`, not "it broke".
- The plain-English column is genuinely theirs. "It expected a closing quote and did not find one" is the standard.
- The change table in Part D shows they ran each variation. Removing the indentation should produce an `IndentationError`, and a trainee who wrote something else did not try it.
- Part E shows a question about **why**, not a request for code.

**Common failures and the fix**

| Problem | What to do |
|---|---|
| Pasted the code from a phone photo of the slide | The point is the typing. Have them delete the cell and type it. Explain why once, kindly. |
| `NameError` they cannot see | Almost always a capital letter: `Print` not `print`, or `Orders` not `orders`. Python is case-sensitive. |
| Indentation errors everywhere | They are fighting Colab's auto-indent. Show them once, on the projector, at normal speed. |
| Cell 2 run before Cell 1 | Classic notebook confusion. Teach "run from the top" now and it never recurs. |
| Asked the assistant to write the whole thing | Not a discipline problem — they were stuck and embarrassed. Sit with them for two minutes; it usually never happens again. |
| "It worked" with nothing written down | The written output is the evidence. Send it back. |

**On the three deliberate errors.** Some trainees resist breaking working code — it feels like vandalism after they finally got it running. Do it on the projector first, cheerfully, and read the error aloud in plain English. Once they see the trainer break something on purpose and shrug, the room relaxes.

**Quick marking scale**

| | |
|---|---|
| **Complete** | Both labs typed and run, three errors recorded with real messages, four variations tried, own-words explanations |
| **Partial** | Code runs but errors or explanations left thin |
| **Not done** | Retype tonight. Day 2 opens with the messy list and assumes the notebook exists. |

**Opening next session:** ask two trainees to read out an error message and what it meant. Then collect messy lists — Day 2's first lab cleans a real one, and it works far better when the data belongs to somebody in the room.
