import express from "express";
import { openai } from "../services/openai.js";

const router = express.Router();

// POST /chat
router.post("/", async (req, res) => {
    try {
        const { message } = req.body;

        const completion = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "user", content: message }],
        });

        res.json({
            reply: completion.choices[0].message.content,
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Something went wrong" });
    }
});

// GET /chat/stream?message=hello
router.get("/stream", async (req, res) => {
    try {
        const { message } = req.query;

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        const stream = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "user", content: message }],
            stream: true,
        });

        for await (const chunk of stream) {
            const content = chunk.choices[0]?.delta?.content || "";
            if (content) {
                res.write(`data: ${content}\n\n`);
            }
        }

        res.write("data: [DONE]\n\n");
        res.end();
    } catch (err) {
        console.error(err);
        res.end();
    }
});

export default router;