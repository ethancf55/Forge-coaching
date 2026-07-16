const GOAL_LABELS = {
  hypertrophy: 'Build muscle / fill out',
  strength: 'Get stronger (SBD or general)',
  recomp: 'Recomp / clean up while lifting',
  'break-plateau': 'Break a plateau',
  other: 'Other',
  // legacy form values
  'fat-loss': 'Fat Loss',
  muscle: 'Build Muscle',
  general: 'General Fitness',
  'active-aging': 'Active Aging',
};

const STATUS_LABELS = {
  natural: 'Natural',
  peptides: 'Peptides',
  enhanced: 'Enhanced',
  'prefer-not': 'Prefer not to say',
};

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
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

  const { firstName, lastName, email, phone, goal, plan, message, status } = req.body || {};

  if (!firstName?.trim() || !lastName?.trim() || !email?.trim() || !goal?.trim()) {
    return res.status(400).json({ error: 'Please fill in all required fields.' });
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email.trim())) {
    return res.status(400).json({ error: 'Please enter a valid email address.' });
  }

  const goalLabel = GOAL_LABELS[goal] || goal;
  const statusLabel = STATUS_LABELS[status] || status || 'Not specified';
  const clientEmail = email.trim();
  const first = firstName.trim();
  const fullName = `${first} ${lastName.trim()}`;
  const safeName = escapeHtml(fullName);
  const safeFirst = escapeHtml(first);
  const safeEmail = escapeHtml(clientEmail);
  const safePhone = escapeHtml(phone?.trim() || 'Not provided');
  const safePlan = escapeHtml(plan?.trim() || 'Not sure yet');
  const safeGoal = escapeHtml(goalLabel);
  const safeStatus = escapeHtml(statusLabel);
  const safeMessage = escapeHtml(message?.trim() || 'No additional message');

  const notifyHtml = `
    <h2>New Forge Coaching application</h2>
    <p><strong>Name:</strong> ${safeName}</p>
    <p><strong>Email:</strong> <a href="mailto:${safeEmail}">${safeEmail}</a></p>
    <p><strong>Phone:</strong> ${safePhone}</p>
    <p><strong>Primary goal:</strong> ${safeGoal}</p>
    <p><strong>Training status:</strong> ${safeStatus}</p>
    <p><strong>Interested plan:</strong> ${safePlan}</p>
    <p><strong>Message:</strong></p>
    <p>${safeMessage.replace(/\n/g, '<br>')}</p>
    <hr>
    <p><em>Submitted from forgevirtualtraining.org</em></p>
  `;

  const confirmationHtml = `
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #1a1a1a; line-height: 1.6; max-width: 560px;">
      <p style="color: #f97316; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; font-size: 12px; margin: 0 0 8px;">Forge Coaching</p>
      <h1 style="font-size: 24px; margin: 0 0 16px;">Application received</h1>
      <p>Hi ${safeFirst},</p>
      <p>Thanks for applying to the <strong>12-Week Forge Program</strong>. I've got your info and will reach out within <strong>24 hours</strong> to schedule a short intro call.</p>
      <p><strong>Here's what you submitted:</strong></p>
      <ul>
        <li><strong>Goal:</strong> ${safeGoal}</li>
        <li><strong>Plan interest:</strong> ${safePlan}</li>
      </ul>
      <p><strong>What to expect on the call:</strong></p>
      <ul>
        <li>We'll talk about your goals, training age, and schedule</li>
        <li>We'll cover equipment and how you currently train</li>
        <li>I'll answer your questions — no pressure, just clarity</li>
      </ul>
      <p>If you need to reach me sooner:</p>
      <ul>
        <li>Email: <a href="mailto:ethanflem1@gmail.com">ethanflem1@gmail.com</a></li>
        <li>Phone / text: <a href="tel:+14694008783">(469) 400-8783</a></li>
        <li>Instagram: <a href="https://instagram.com/85ethan_">@85ethan_</a></li>
      </ul>
      <p>Talk soon,<br><strong>Ethan Fleming</strong><br>Forge Coaching<br><a href="https://forgevirtualtraining.org">forgevirtualtraining.org</a></p>
    </div>
  `;

  try {
    await sendEmail(apiKey, {
      from: fromEmail,
      to: [notifyEmail],
      reply_to: clientEmail,
      subject: `New consult: ${fullName}`,
      html: notifyHtml,
    });

    try {
      await sendEmail(apiKey, {
        from: fromEmail,
        to: [clientEmail],
        reply_to: notifyEmail,
        subject: 'Your Forge Coaching consultation request',
        html: confirmationHtml,
      });
    } catch (confirmError) {
      console.error('Confirmation email failed:', confirmError.message);
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Contact form error:', error.message);
    return res.status(500).json({ error: 'Failed to send your request. Please email ethanflem1@gmail.com directly.' });
  }
};