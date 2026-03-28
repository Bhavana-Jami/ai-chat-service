import express from "express";
import cors from "cors";
import chatRoutes from "./src/routes/chat.js";

const app = express();

app.use(cors());
app.use(express.json());

app.use("/chat", chatRoutes);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});