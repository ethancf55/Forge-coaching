function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function nl2br(value) {
  return escapeHtml(value).replace(/\n/g, '<br>');
}

async function sendEmail(apiKey, payload) {
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Resend ${response.status}: ${errorBody}`);
  }

  return response.json();
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  const notifyEmail = process.env.NOTIFY_EMAIL || 'ethanflem1@gmail.com';
  const fromEmail = process.env.FROM_EMAIL || 'Forge Coaching <onboarding@resend.dev>';

  if (!apiKey) {
    console.error('RESEND_API_KEY is not configured');
    return res.status(500).json({ error: 'Email service is not configured yet.' });
  }

  const body = req.body || {};

  // Support new intake fields + older form field names
  const fullName = (body.fullName || [body.firstName, body.lastName].filter(Boolean).join(' ')).trim();
  const email = String(body.email || '').trim();
  const age = String(body.age || '').trim();
  const goal = String(body.goal || '').trim();
  const trainingYears = String(body.trainingYears || '').trim();
  const daysPerWeek = String(body.daysPerWeek || '').trim();
  const equipment = String(body.equipment || body.message || '').trim();
  const injuries = String(body.injuries || '').trim();
  const status = String(body.status || '').trim();
  const source = String(body.source || body.plan || 'Website intake form').trim();

  if (!fullName || !email || !age || !goal || !trainingYears || !daysPerWeek || !equipment || !injuries || !status) {
    return res.status(400).json({ error: 'Please fill in all required fields.' });
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    return res.status(400).json({ error: 'Please enter a valid email address.' });
  }

  const ageNum = Number(age);
  if (!Number.isFinite(ageNum) || ageNum < 13 || ageNum > 99) {
    return res.status(400).json({ error: 'Please enter a valid age.' });
  }

  const first = fullName.split(/\s+/)[0] || fullName;
  const safe = {
    fullName: escapeHtml(fullName),
    first: escapeHtml(first),
    email: escapeHtml(email),
    age: escapeHtml(age),
    goal: escapeHtml(goal),
    trainingYears: escapeHtml(trainingYears),
    daysPerWeek: escapeHtml(daysPerWeek),
    equipment: nl2br(equipment),
    injuries: nl2br(injuries),
    status: escapeHtml(status),
    source: escapeHtml(source),
  };

  const notifyHtml = `
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #111; line-height: 1.55; max-width: 640px;">
      <p style="color: #f97316; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; font-size: 12px; margin: 0 0 8px;">Forge Coaching</p>
      <h2 style="margin: 0 0 16px;">New client intake submission</h2>
      <p style="margin: 0 0 16px; color: #555;">Someone submitted the intake form on forgevirtualtraining.org</p>
      <table style="width: 100%; border-collapse: collapse; font-size: 15px;">
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; width: 42%; color: #666;"><strong>1. Full Name</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.fullName}</td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666;"><strong>2. Email</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;"><a href="mailto:${safe.email}">${safe.email}</a></td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666;"><strong>3. Age</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.age}</td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666;"><strong>4. Main goal</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.goal}</td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666;"><strong>5. Training history</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.trainingYears}</td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666;"><strong>6. Days / week</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.daysPerWeek}</td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666; vertical-align: top;"><strong>7. Gym / equipment</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.equipment}</td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666; vertical-align: top;"><strong>8. Injuries / limits</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.injuries}</td></tr>
        <tr><td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #666;"><strong>9. Natural / peptides / enhanced</strong></td><td style="padding: 10px 0; border-bottom: 1px solid #eee;">${safe.status}</td></tr>
        <tr><td style="padding: 10px 0; color: #666;"><strong>Source / interest</strong></td><td style="padding: 10px 0;">${safe.source}</td></tr>
      </table>
      <p style="margin: 20px 0 0; color: #888; font-size: 13px;">Reply directly to this email to respond to the client.</p>
    </div>
  `;

  const confirmationHtml = `
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #1a1a1a; line-height: 1.6; max-width: 560px;">
      <p style="color: #f97316; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; font-size: 12px; margin: 0 0 8px;">Forge Coaching</p>
      <h1 style="font-size: 22px; margin: 0 0 16px;">Intake received</h1>
      <p>Hi ${safe.first},</p>
      <p>Thanks for submitting your client intake form. I’ve got your answers and will review them, then follow up within <strong>24 hours</strong>.</p>
      <p><strong>What you sent:</strong></p>
      <ul>
        <li><strong>Goal:</strong> ${safe.goal}</li>
        <li><strong>Training days:</strong> ${safe.daysPerWeek}/week</li>
        <li><strong>Age:</strong> ${safe.age}</li>
      </ul>
      <p>If you need to reach me sooner:</p>
      <ul>
        <li>Email: <a href="mailto:ethanflem1@gmail.com">ethanflem1@gmail.com</a></li>
        <li>Phone / text: <a href="tel:+14694008783">(469) 400-8783</a></li>
        <li>Instagram: <a href="https://instagram.com/85ethan_ol">@85ethan_ol</a></li>
      </ul>
      <p>Talk soon,<br><strong>Ethan Fleming</strong><br>Forge Coaching<br><a href="https://forgevirtualtraining.org">forgevirtualtraining.org</a></p>
      <p style="color: #888; font-size: 12px; margin-top: 24px;">This information is for coaching purposes only and is not medical advice.</p>
    </div>
  `;

  try {
    await sendEmail(apiKey, {
      from: fromEmail,
      to: [notifyEmail],
      reply_to: email,
      subject: `New intake: ${fullName} · ${goal} · age ${age}`,
      html: notifyHtml,
    });

    try {
      await sendEmail(apiKey, {
        from: fromEmail,
        to: [email],
        reply_to: notifyEmail,
        subject: 'Forge Coaching — intake received',
        html: confirmationHtml,
      });
    } catch (confirmError) {
      console.error('Confirmation email failed:', confirmError.message);
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Contact form error:', error.message);
    return res.status(500).json({
      error: 'Failed to send your form. Please email ethanflem1@gmail.com directly.',
    });
  }
};
