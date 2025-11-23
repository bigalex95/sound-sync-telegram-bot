# Free Hosting Options for Telegram Bots

You cannot use **GitHub Actions** to host your bot. GitHub Actions is designed for *running tasks* (like building your code or testing it), not for *hosting long-running applications*. If you try to run a bot there, it will be terminated after 6 hours, and you risk getting your account banned for violating the Terms of Service.

However, there are several excellent free (or free-tier) options where you can deploy your Docker container.

## 1. Oracle Cloud "Always Free" (Recommended)
Oracle offers the most generous free tier.
- **Specs**: Up to 4 ARM Ampere instances with 24 GB of RAM (total).
- **Pros**: Actual VPS (Ubuntu/Linux), very powerful, completely free indefinitely.
- **Cons**: Sign-up can be difficult (cards often rejected), interface is complex.
- **Deployment**: You get a full Linux server. Follow the [Deployment Guide](deployment.md).

> [!NOTE]
> **Why 4 CPUs matter:**
> Even though Python is single-threaded, this bot spawns external processes for `yt-dlp` and `ffmpeg`. These tools **WILL** use multiple CPU cores for downloading and converting audio. Having 4 CPUs means you can handle multiple heavy downloads simultaneously much faster.

## 2. Fly.io
Great for Docker apps.
- **Free Allowance**: They have a free allowance for small apps (up to 3 shared-cpu-1x 256mb VMs). *Note: They have moved to a usage-based model but often give free credits or have low costs.*
- **Pros**: Extremely easy to deploy (`fly launch`), native Docker support.
- **Cons**: The "free" tier is now a bit more complex (often requires credit card and might cost pennies if you exceed limits).

## 3. Render.com
- **Free Tier**: Offers free Web Services (spins down after inactivity) and Background Workers (paid).
- **Workaround**: You can use a free Web Service and use a service like UptimeRobot to ping it to keep it awake, but this is not ideal for a Telegram bot using polling.
- **Pros**: Very easy to use.

## 4. Google Cloud Platform (GCP) Free Tier
- **Specs**: e2-micro instance (2 vCPUs, 1 GB memory).
- **Pros**: Reliable, industry standard.
- **Cons**: Limited bandwidth (network egress costs can add up if you download/upload huge files), 1GB RAM might be tight for `yt-dlp` + `ffmpeg` on heavy videos.

## 5. Amazon AWS Free Tier
- **Specs**: t2.micro or t3.micro EC2 instance.
- **Pros**: Industry standard.
- **Cons**: Free for only **12 months**.

## Summary Recommendation

1.  **Best Performance**: **Oracle Cloud** (if you can get an account).
2.  **Easiest to Deploy**: **Fly.io** (install `flyctl`, login, `fly launch`).
3.  **Standard VPS**: **AWS** or **GCP** (requires setting up a Linux server like in our Deployment Guide).
