#!/usr/bin/env python3
"""Generate educational harm-reduction PDF guide for young lifters."""

from pathlib import Path
from fpdf import FPDF


OUTPUT = Path(__file__).resolve().parent / "What-Most-Young-Lifters-Get-Wrong-About-PEDs-Hormones.pdf"

# Letter size in mm
PAGE_W = 215.9
PAGE_H = 279.4
MARGIN_L = 18
MARGIN_R = 18
MARGIN_T = 18
MARGIN_B = 20
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R  # ~179.9


class GuidePDF(FPDF):
    def __init__(self):
        super().__init__(unit="mm", format="letter")
        self.set_margins(MARGIN_L, MARGIN_T, MARGIN_R)
        self.set_auto_page_break(auto=True, margin=MARGIN_B)
        self.section_num = 0

    # ----- helpers -----
    def content_bottom(self):
        """Y coordinate where body text must stop (above footer)."""
        return PAGE_H - MARGIN_B

    def remaining_height(self):
        return self.content_bottom() - self.get_y()

    def ensure_space(self, height_mm):
        """Start a new page if the next block won't fit cleanly."""
        if self.get_y() + height_mm > self.content_bottom() - 2:
            self.add_page()

    def usable_width(self):
        return CONTENT_W

    def reset_x(self):
        self.set_x(MARGIN_L)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(10)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.reset_x()
        self.cell(CONTENT_W, 5, "What Most Young Lifters Get Wrong About PEDs & Hormones", align="L")
        self.ln(5)
        self.set_draw_color(220, 220, 220)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
        self.ln(8)
        # Keep body below header band
        if self.get_y() < 24:
            self.set_y(24)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        self.reset_x()
        self.cell(
            CONTENT_W,
            6,
            f"Educational only  |  Page {self.page_no()}/{{nb}}  |  Not medical advice",
            align="C",
        )

    def cover(self):
        self.add_page()
        self.ln(32)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(230, 100, 20)
        self.reset_x()
        self.cell(CONTENT_W, 8, "FORGE COACHING  -  DIGITAL GUIDE", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)
        self.set_text_color(20, 20, 20)
        self.set_font("Helvetica", "B", 24)
        self.reset_x()
        self.multi_cell(CONTENT_W, 11, "What Most Young Lifters\nGet Wrong About\nPEDs & Hormones", align="C")
        self.ln(6)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(70, 70, 70)
        self.reset_x()
        self.multi_cell(
            CONTENT_W,
            6.5,
            "An educational, harm-reduction guide for serious lifters ages 18-28.\n"
            "Natural - Considering peptides - Or already enhanced.",
            align="C",
        )
        self.ln(10)
        self.set_draw_color(230, 100, 20)
        self.set_line_width(0.6)
        mid_y = self.get_y()
        self.line(PAGE_W / 2 - 35, mid_y, PAGE_W / 2 + 35, mid_y)
        self.ln(10)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(90, 90, 90)
        self.reset_x()
        self.multi_cell(
            CONTENT_W,
            5.5,
            "This guide does not teach you how to use PEDs or peptides.\n"
            "It is not medical advice. It will not tell you what to take, how much to take,\n"
            "where to get anything, or how to inject or administer anything.\n\n"
            "It is about thinking clearly, understanding risk, and making better decisions.",
            align="C",
        )
        self.ln(14)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.reset_x()
        self.cell(CONTENT_W, 6, "Evidence-informed  -  Direct  -  Anti-hype", align="C", new_x="LMARGIN", new_y="NEXT")

    def toc(self, items):
        self.add_page()
        self.heading("Contents")
        self.ln(1)
        for i, title in enumerate(items, 1):
            self.ensure_space(10)
            self.set_font("Helvetica", "", 10.5)
            self.set_text_color(40, 40, 40)
            self.reset_x()
            # Wrap long TOC lines instead of overflowing
            label = f"{i}.  {title}"
            self.multi_cell(CONTENT_W, 6.5, label)
            self.ln(1)
        self.ln(4)
        self.callout(
            "How to use this guide",
            "Read it in order once. Then revisit the Decision Framework anytime someone online "
            "makes enhancement sound simple, inevitable, or risk-free.",
        )

    def heading(self, text):
        self.ensure_space(22)
        self.reset_x()
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(20, 20, 20)
        self.multi_cell(CONTENT_W, 7.5, text)
        self.ln(2)
        self.set_draw_color(230, 100, 20)
        self.set_line_width(0.5)
        y = self.get_y()
        self.line(MARGIN_L, y, MARGIN_L + 40, y)
        self.ln(5)

    def subheading(self, text):
        self.ensure_space(16)
        self.ln(1)
        self.reset_x()
        self.set_font("Helvetica", "B", 11.5)
        self.set_text_color(35, 35, 35)
        self.multi_cell(CONTENT_W, 6.5, text)
        self.ln(2)

    def body(self, text):
        self.ensure_space(12)
        self.reset_x()
        self.set_font("Helvetica", "", 10)
        self.set_text_color(45, 45, 45)
        self.multi_cell(CONTENT_W, 5.4, text)
        self.ln(2.5)

    def bullet(self, items):
        bullet_indent = 6
        text_w = CONTENT_W - bullet_indent
        for item in items:
            # Estimate lines for ensure_space
            self.set_font("Helvetica", "", 10)
            approx_lines = max(1, int(self.get_string_width(item) / text_w) + 1)
            self.ensure_space(approx_lines * 5.4 + 4)

            y0 = self.get_y()
            self.reset_x()
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(230, 100, 20)
            self.cell(bullet_indent, 5.4, "-")

            self.set_xy(MARGIN_L + bullet_indent, y0)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(45, 45, 45)
            self.multi_cell(text_w, 5.4, item)
            self.ln(1.5)
        self.ln(1.5)

    def callout(self, title, text):
        """Draw a callout that always stays fully on one page when possible."""
        pad = 4
        inner_w = CONTENT_W - 2 * pad

        self.set_font("Helvetica", "B", 10)
        title_h = self._text_height(title, inner_w, 5.5)
        self.set_font("Helvetica", "", 9.5)
        body_h = self._text_height(text, inner_w, 5.2)
        box_h = pad + title_h + 2 + body_h + pad

        self.ensure_space(box_h + 4)
        self.ln(1)

        x = MARGIN_L
        y = self.get_y()

        # Background
        self.set_fill_color(252, 246, 240)
        self.set_draw_color(230, 100, 20)
        self.set_line_width(0.4)
        self.rect(x, y, CONTENT_W, box_h, style="DF")

        # Accent bar on left
        self.set_fill_color(230, 100, 20)
        self.rect(x, y, 1.8, box_h, style="F")

        # Title
        self.set_xy(x + pad, y + pad)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(180, 80, 15)
        self.multi_cell(inner_w, 5.5, title)

        # Body
        self.set_x(x + pad)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(55, 55, 55)
        self.multi_cell(inner_w, 5.2, text)

        self.set_y(y + box_h + 4)

    def _text_height(self, text, width, line_h):
        """Estimate multi_cell height for current font."""
        if not text:
            return line_h
        # Word-wrap estimate using fpdf string width
        words = text.replace("\n", " \n ").split(" ")
        lines = 1
        line = ""
        for w in words:
            if w == "\n":
                lines += 1
                line = ""
                continue
            test = (line + " " + w).strip()
            if self.get_string_width(test) <= width:
                line = test
            else:
                lines += 1
                line = w
        return lines * line_h

    def section(self, title):
        self.section_num += 1
        self.add_page()
        self.ensure_space(28)
        self.reset_x()
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(230, 100, 20)
        self.cell(CONTENT_W, 5, f"SECTION {self.section_num}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.heading(title)

    def disclaimer_block(self, text):
        """Full disclaimer that can paginate cleanly."""
        self.ensure_space(20)
        self.reset_x()
        self.set_fill_color(35, 35, 38)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(CONTENT_W, 9, "  STRONG DISCLAIMER - READ CAREFULLY", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.reset_x()
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "", 9.5)
        # Split into paragraphs so page breaks work mid-disclaimer
        for para in text.split("\n\n"):
            self.ensure_space(14)
            self.reset_x()
            self.multi_cell(CONTENT_W, 5.2, para)
            self.ln(3)


def build():
    pdf = GuidePDF()
    pdf.alias_nb_pages()

    sections = [
        "Introduction - Why this guide exists",
        "The reality of natural potential vs. enhanced expectations",
        "Why so many young guys make poor decisions with PEDs/peptides",
        "Why results and side effects vary so widely between people",
        "Bloodwork and health monitoring (high-level education only)",
        "Common myths young guys believe about first cycles",
        "How training and recovery actually change when enhanced (general principles only)",
        "Why most online advice is low-quality or reckless",
        "Decision framework - questions to ask before considering enhancement",
        "Final thoughts + strong disclaimer",
    ]

    # ----- COVER & TOC -----
    pdf.cover()
    pdf.toc(sections)

    # ----- 1 -----
    pdf.section(sections[0])
    pdf.body(
        "If you train hard in your late teens or twenties, you're going to run into PED and peptide talk. "
        "Not from a doctor. From Instagram, TikTok, gym conversations, and comment sections that turn "
        "chemistry into clout."
    )
    pdf.body(
        "Most of that conversation is optimized for engagement, not for your long-term health or actual "
        "progress. Young lifters are ambitious and impatient - and that combination is easy to exploit "
        "with before-and-after photos, certainty, and incomplete stories."
    )
    pdf.subheading("What this is")
    pdf.bullet(
        [
            "An educational, harm-reduction resource about how people think about PEDs, peptides, and hormones.",
            "A tool for clearer thinking: expectations, risk, variability, and decision quality.",
            "Useful whether you're natural, curious, or already enhanced - because the thinking problem is the same.",
        ]
    )
    pdf.subheading("What this is not")
    pdf.bullet(
        [
            "Not a how-to guide. No dosing, stacks, sources, or administration instructions.",
            "Not medical advice. Nothing here diagnoses, treats, or recommends use of any substance.",
            "Not a fear campaign. Scare tactics are just as dishonest as hype.",
            "Not a pitch to use PEDs. Enhancement is not required to train hard or make progress.",
        ]
    )
    pdf.callout(
        "Core stance",
        "Good decisions start with accurate models of risk, recovery, and incentives - "
        "not with secret protocols from anonymous accounts.",
    )

    # ----- 2 -----
    pdf.section(sections[1])
    pdf.body(
        "A large share of frustration in young lifters comes from a broken comparison: your real "
        "body, training age, sleep, and genetics versus someone else's highlight reel - often "
        "under different pharmacology, lighting, drugs, years of training, and sometimes photo "
        "editing or peak-week presentation."
    )
    pdf.subheading("Natural potential is real - and unevenly distributed")
    pdf.body(
        "People differ in muscle insertions, frame, recovery capacity, hormone baseline ranges, "
        "injury history, and how they respond to progressive training. Two honest natural lifters "
        "with the same program can look and perform differently after three years. That is not "
        "a moral failure. It is biology plus time."
    )
    pdf.body(
        "Natural progress is usually nonlinear: big early gains, then harder-earned improvements. "
        "When that slowdown hits, enhancement marketing gets louder - not because nature 'ended,' "
        "but because patience becomes expensive and social media rewards shortcuts."
    )
    pdf.subheading("Enhanced outcomes are not a guaranteed upgrade")
    pdf.body(
        "Pharmacology can change the rate of adaptation and the amount of training stress someone "
        "can recover from - for some people, under some conditions. It can also create side effects, "
        "dependency on ongoing management, legal risk (depending on jurisdiction and substances), "
        "financial cost, and identity confusion when results feel inseparable from the drug."
    )
    pdf.bullet(
        [
            "Enhancement does not fix bad programming, bad sleep, or chaotic eating.",
            "It does not guarantee the physique you imagined from someone else's photos.",
            "It can raise expectations so high that normal progress feels like failure.",
            "Coming off can feel like regression even when you still trained hard - psychologically and sometimes physiologically.",
        ]
    )
    pdf.callout(
        "Expectation audit",
        "Ask: 'What would a good natural year look like for me with perfect consistency?' "
        "If you cannot answer that, you do not yet have a baseline for judging enhancement claims.",
    )

    # ----- 3 -----
    pdf.section(sections[2])
    pdf.body(
        "Poor decisions rarely look like 'I want to be reckless.' They look like urgency, envy, "
        "and incomplete information dressed up as confidence."
    )
    pdf.subheading("Common drivers of bad decisions")
    pdf.bullet(
        [
            "Social comparison: constant exposure to outliers and undisclosed enhancement.",
            "Identity pressure: 'serious lifter' culture that treats natural progress as lesser.",
            "Impatience: wanting a 5-year look in 12 months without owning the tradeoffs.",
            "Information chaos: forums, influencers, and private chats with no accountability.",
            "Sunk cost: years of training without clear structure, then looking for a 'missing chemical' explanation.",
            "All-or-nothing thinking: 'everyone does it' or 'I'll be left behind.' Both are usually false.",
        ]
    )
    pdf.subheading("Peptides vs. 'harder' PEDs in the young-guy conversation")
    pdf.body(
        "Online culture often markets peptides as softer, smarter, or more modern - and markets "
        "classic anabolic PEDs as obvious if you are 'serious.' That framing is marketing, not a "
        "safety certificate. Different compounds have different risk profiles, evidence bases, "
        "legal statuses, and unknowns. 'Not a steroid' is not the same as 'low risk' or 'well studied "
        "for healthy young men who lift.'"
    )
    pdf.body(
        "Young guys also underestimate how easily curiosity becomes a pipeline: research as entertainment, "
        "then 'just one thing,' then escalation when results do not match fantasy timelines. Harm reduction "
        "means noticing that pipeline early - before identity depends on it."
    )
    pdf.callout(
        "Pattern to watch",
        "If your training plan is inconsistent but your research into enhancement is daily, "
        "you may be solving the wrong problem first.",
    )

    # ----- 4 -----
    pdf.section(sections[3])
    pdf.body(
        "One of the most dangerous myths is: 'If it worked for him, it will work the same for me - "
        "and the side effects will be the same too.' Bodies are not copy-paste."
    )
    pdf.subheading("Why outcomes differ so much")
    pdf.bullet(
        [
            "Genetics and receptor-level biology: people respond differently to the same stimulus - training or pharmacology.",
            "Age and developmental stage: younger systems are still adapting; long-term data for many practices is incomplete.",
            "Training age and tissue readiness: connective tissue, skill, and work capacity do not always keep up with muscle growth rate.",
            "Sleep, stress, alcohol, and life load: recovery is systemic, not just 'gym recovery.'",
            "Nutrition quality and total intake: enhancement does not replace energy balance fundamentals.",
            "Undisclosed polypharmacy: what people report as 'one compound' is sometimes multiple variables.",
            "Reporting bias: people share PRs and photos; fewer share labs, anxiety, sexual side effects, or regret.",
            "Placebo and expectation: belief changes how hard people train and how they interpret change.",
        ]
    )
    pdf.subheading("Side effects are not a character test")
    pdf.body(
        "Some people experience few noticeable short-term issues and conclude everything is fine. "
        "Some experience blood pressure changes, lipid issues, mood changes, acne, sleep disruption, "
        "suppression of natural hormone production pathways, fertility concerns, or other problems - "
        "and those problems may show up later or only on labs. Absence of a dramatic story is not "
        "proof of safety. Presence of a dramatic story is not proof every user will share it."
    )
    pdf.callout(
        "Intellectual honesty",
        "If someone cannot explain why results and risks vary between people, they are selling certainty, "
        "not educating you.",
    )

    # ----- 5 -----
    pdf.section(sections[4])
    pdf.body(
        "This section is high-level education only. It is not a protocol, a lab panel prescription, "
        "or a substitute for a licensed clinician. If you have health concerns, work with qualified medical professionals."
    )
    pdf.subheading("Why monitoring concepts matter")
    pdf.body(
        "Hormones and many PEDs/peptides interact with systems you cannot fully 'feel': blood lipids, "
        "red blood cell related markers, liver enzymes, blood pressure, endocrine feedback loops, and more. "
        "Subjective feel - pumps, libido, mood - is incomplete data. People who treat self-experimentation "
        "as science without measurement are not doing science; they are doing hope with a logbook."
    )
    pdf.subheading("What 'bloodwork thinking' actually means")
    pdf.bullet(
        [
            "Baseline before big changes: knowing your normal is more useful than a single scary or comforting number later.",
            "Trends over time beat one-off screenshots shared without context.",
            "Reference ranges are population tools, not personal destiny - interpretation needs clinical context.",
            "Self-ordering labs without medical follow-up can create false reassurance or unhelpful panic.",
            "Health monitoring is broader than hormones: blood pressure, sleep quality, resting heart rate trends, mood, and sexual health matter.",
        ]
    )
    pdf.subheading("What this section will not do")
    pdf.body(
        "It will not tell you which markers to force, what numbers are 'fine for a cycle,' how to 'fix' labs, "
        "or how to self-medicate based on results. Those are clinical and often reckless DIY patterns. "
        "If monitoring matters to you, the responsible path is clinician-guided care - not forum-guided care."
    )
    pdf.callout(
        "Harm-reduction framing",
        "If someone recommends pharmacology but dismisses medical oversight, blood pressure, or long-term "
        "endocrine consequences, treat their confidence as a red flag.",
    )

    # ----- 6 -----
    pdf.section(sections[5])
    pdf.body(
        "First-cycle mythology is a genre. It spreads because it's simple, masculine-coded, and easy to meme. "
        "Here are the patterns that show up constantly among young guys - framed as myths, not as how-to corrections."
    )
    pdf.subheading('Myth: "I\'ll just do a little to jump-start, then stay natural forever"')
    pdf.body(
        "Some people do stop. Many discover that returning to previous rates of progress feels disappointing, "
        "or that their identity has already shifted. Planning for \"temporary\" without planning for the "
        "psychology and health follow-through is incomplete decision-making."
    )
    pdf.subheading('Myth: "If I train hard enough, side effects won\'t matter"')
    pdf.body(
        "Effort in the gym does not cancel systemic effects. Training hard is good. It is not a medical shield."
    )
    pdf.subheading('Myth: "Young guys recover from anything"')
    pdf.body(
        "Youth can mean resilience in some areas and vulnerability in others. Developing bodies and brains "
        "are not free risk-erasure coupons. Long-term data is often thinner than influencers imply."
    )
    pdf.subheading('Myth: "Everyone who looks like that is on something - so I have to be too"')
    pdf.body(
        "Some high-level physiques involve enhancement. Many impressive lifters are natural. Many enhanced "
        "lifters still look average because drugs do not install discipline. All-or-nothing narratives are "
        "usually for engagement, not truth."
    )
    pdf.subheading('Myth: "Peptides / SARMs / research chemicals are basically harmless alternatives"')
    pdf.body(
        "Different substances have different risks, evidence quality, and legal contexts. Marketing language "
        "like \"research,\" \"natural boost,\" or \"not a steroid\" can create a false safety halo. Unknowns and "
        "quality-control problems are themselves risks."
    )
    pdf.subheading('Myth: "I\'ll know if something is wrong"')
    pdf.body(
        "Some issues announce themselves. Others are silent until labs or a blood pressure cuff say otherwise. "
        "Waiting for dramatic symptoms is not a monitoring strategy."
    )
    pdf.subheading('Myth: "PCT / recovery talk online means the plan is responsible"')
    pdf.body(
        "Online recovery chatter is often incomplete, copy-pasted, or mismatched to the individual. "
        "The existence of a popular narrative does not equal medical appropriateness. This guide will not "
        "provide recovery protocols - only the warning that forum consensus is not clinical care."
    )
    pdf.callout(
        "Myth filter",
        "If a claim removes uncertainty, cost, regret, or individual variability, it is probably "
        "designed to close the sale - not to educate.",
    )

    # ----- 7 -----
    pdf.section(sections[6])
    pdf.body(
        "This section is general principles only. It is not a program template and not encouragement to enhance. "
        "It exists because young lifters often assume enhancement 'just multiplies gains' while leaving "
        "everything else the same. That model is too crude."
    )
    pdf.subheading("Adaptation still depends on stimulus and recovery")
    pdf.body(
        "Regardless of natural or enhanced status, muscle and strength adaptations still require progressive "
        "tension, enough total work over time, skill practice on lifts, and recovery resources (sleep, food, "
        "stress management). Pharmacology does not replace the training process; at most it can change "
        "how much stress you can tolerate and how quickly some adaptations accumulate for some people."
    )
    pdf.subheading("Tissue stress is not only muscle stress")
    pdf.body(
        "A classic failure mode: muscular recovery outpaces tendons, ligaments, joints, or movement skill. "
        "People add load faster than connective tissues and technique can absorb. The result can be pain, "
        "injury, or stalled long-term progress. Smart training still manages volume, intensity, and exercise "
        "selection - especially when ego strength climbs quickly."
    )
    pdf.subheading("Recovery is a system")
    pdf.body(
        "When people can train more frequently or more aggressively, they often under-invest in the boring "
        "multipliers: sleep regularity, protein and total calories, step count vs. junk volume, alcohol, "
        "and stress. Enhancement culture sometimes glorifies brutality and underplays monotony. "
        "Monotony is where careers are built."
    )
    pdf.subheading("Psychology of training while enhanced")
    pdf.bullet(
        [
            "PR chasing can replace process focus.",
            "Coming off or reducing pharmacology can feel like identity threat if self-worth was scoreboard-only.",
            "Comparison does not stop after enhancement; the reference group just changes.",
            "Natural skills - patience, technique, program adherence - remain high-ROI either way.",
        ]
    )
    pdf.callout(
        "Principle",
        "If someone cannot train intelligently natural, enhancement usually amplifies chaos faster than it "
        "amplifies excellence.",
    )

    # ----- 8 -----
    pdf.section(sections[7])
    pdf.body(
        "Most online PED/peptide content is not peer-reviewed education. It is entertainment, status, "
        "affiliate incentives, or identity performance. That does not mean every creator is lying. "
        "It means incentives are misaligned with your long-term welfare."
    )
    pdf.subheading("Why the feed is so bad")
    pdf.bullet(
        [
            "Algorithms reward certainty and extremes, not cautious probability statements.",
            "Before/after content hides genetics, drugs, lighting, pump, dehydration, and years of training age.",
            "Anonymity lowers accountability for bad advice.",
            "Selling coaching, labs, or 'education' can bias recommendations toward complexity and dependency.",
            "Survivorship bias: people who quit after side effects post less than people who got a good photo.",
            "Legal and platform pressure pushes vague language that sounds safer than it is.",
        ]
    )
    pdf.subheading("How to read claims like an adult")
    pdf.bullet(
        [
            "Ask what would falsify the claim.",
            "Separate 'this happened to me' from 'this will happen to you.'",
            "Watch for missing denominators: how many people tried and disliked the outcome?",
            "Prefer sources that discuss tradeoffs, unknowns, and medical involvement over sources that only discuss gains.",
            "Be extra skeptical of anyone who needs you slightly afraid of being left behind.",
        ]
    )
    pdf.callout(
        "Quality test",
        "High-quality education increases your ability to say no. Low-quality content increases your fear "
        "of missing out.",
    )

    # ----- 9 -----
    pdf.section(sections[8])
    pdf.body(
        "If you are natural and curious, use this as a brake pedal. If you are already enhanced, use it "
        "to audit whether your decisions are deliberate or just drift. This is not a permission slip. "
        "It is a thinking checklist."
    )
    pdf.subheading("A. Motivation and identity")
    pdf.bullet(
        [
            "Am I trying to solve training, nutrition, sleep, or patience - with chemistry?",
            "Would I still want this if nobody else could see my body?",
            "Am I okay if results are average and side effects are not?",
            "Whose opinion am I optimizing for?",
        ]
    )
    pdf.subheading("B. Baseline competence")
    pdf.bullet(
        [
            "Have I trained consistently for years with progressive structure, or only sporadically?",
            "Can I explain my program's progression model without copying a random spreadsheet?",
            "Is my sleep and food intake actually good enough that \"optimization\" is the bottleneck?",
            "Have I had injuries that already limit training - and have I addressed them?",
        ]
    )
    pdf.subheading("C. Risk, legality, and life context")
    pdf.bullet(
        [
            "Do I understand legal risks where I live, including possession and testing contexts (sport, work, military, etc.)?",
            "Am I prepared for financial cost beyond the first-purchase narrative?",
            "What happens to school, work, relationships, or sport eligibility if something goes wrong?",
            "Do I have a real medical professional I can talk to honestly - not only anonymous chat?",
        ]
    )
    pdf.subheading("D. Health and uncertainty")
    pdf.bullet(
        [
            "Am I treating unknown long-term risks as zero because they are invisible today?",
            "If I needed to stop for health reasons, would I cope without shame spirals?",
            "Am I confusing \"I read a lot\" with \"I understand clinical risk\"?",
            "Would I accept the same level of uncertainty for a decision about fertility, mood, or cardiovascular health?",
        ]
    )
    pdf.subheading("E. Exit and ethics")
    pdf.bullet(
        [
            "What is my definition of enough?",
            "If I enhance, will I disclose honestly in contexts where others might copy me?",
            "Am I okay never knowing what my natural ceiling would have been?",
            "Can I respect natural lifters - including future me - without contempt?",
        ]
    )
    pdf.callout(
        "Decision rule of thumb",
        "If you cannot write clear answers to these questions without sounding like a sales page, "
        "you are not ready to make a high-stakes body decision. Wait. Train. Reassess later.",
    )

    # ----- 10 -----
    pdf.section(sections[9])
    pdf.body(
        "The iron does not require PEDs. Serious training requires honesty: about effort, recovery, time, "
        "and the stories you tell yourself when progress slows."
    )
    pdf.body(
        "Young lifters get this wrong when they treat enhancement as destiny, peer pressure as evidence, "
        "or online certainty as expertise. The antidote is not panic. It is standards: for information, "
        "for medical reality, for patience, and for what kind of man you become when nobody is watching."
    )
    pdf.body(
        "If you stay natural, that can be a strong, deliberate identity - not a participation trophy. "
        "If you have already used PEDs or peptides, harm reduction still matters: medical care, honest "
        "self-assessment, and refusing to recruit others with incomplete stories."
    )
    pdf.subheading("Carry these ideas forward")
    pdf.bullet(
        [
            "Compare less. Measure your own trends.",
            "Fix training and recovery before romanticizing chemistry.",
            "Assume variability in results and side effects.",
            "Treat anonymous certainty as low-quality by default.",
            "Use the decision framework under pressure - especially then.",
        ]
    )
    pdf.ln(3)
    pdf.disclaimer_block(
        "This document is for educational and harm-reduction purposes only. It does not constitute medical "
        "advice, diagnosis, treatment, or a recommendation to use any performance-enhancing drug, hormone, "
        "peptide, research chemical, supplement, or related product.\n\n"
        "Nothing in this guide should be interpreted as instructions for dosing, stacking, cycling, sourcing, "
        "purchasing, manufacturing, or administering any substance. Do not use this guide to self-medicate "
        "or to design a pharmacology plan.\n\n"
        "Performance-enhancing substances can carry serious legal, health, and personal risks. Individual "
        "responses vary. Online information is frequently incomplete, biased, or wrong.\n\n"
        "Always consult a licensed medical professional for questions about your health, hormones, labs, "
        "medications, or any substance use. If you are in crisis or experiencing a medical emergency, seek "
        "emergency care immediately.\n\n"
        "By reading this guide, you acknowledge that you are responsible for your own decisions and that the "
        "author and publisher assume no liability for actions taken based on this educational material.\n\n"
        "Train hard. Think clearly. Protect your future self."
    )
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.reset_x()
    pdf.cell(CONTENT_W, 6, "Forge Coaching  -  Educational digital product  -  Not medical advice", align="C")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    print(f"Wrote {OUTPUT}")
    print(f"Pages: {pdf.page_no()}")
    print(f"Size: {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    build()
