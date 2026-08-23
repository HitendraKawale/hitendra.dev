export const profile = {
  name: "Hitendra Kawale",
  initials: "HK",
  title: "AI Engineer",
  bio: "MSc Artificial Intelligence (University of Surrey). I build production-grade AI systems — LLM platforms, RAG pipelines, and interactive 3D vision — backend-heavy, deployment-aware, and obsessed with what holds up in the real world. I'm also a polyglot: I work comfortably in English and Spanish, hold a conversation in Mandarin, carry Hindi and Marathi as mother tongues, and read or speak a half-dozen more. Global teams and international users feel like home.",
  availability: "Open to AI roles and freelance work",

  // Short form for social cards, which truncate around 150 characters.
  cardBio:
    "AI engineer — LLM platforms, RAG pipelines, and 3D vision. MSc Artificial Intelligence, Surrey. Polyglot across eight languages.",

  // Links
  github: "https://github.com/HitendraKawale",
  codeberg: "https://codeberg.org/HitendraKawale",
  linkedin: "https://linkedin.com/in/hitendra-kawale",
  email: "hituhitesh303@gmail.com",
  resume: "/resume.pdf",  // served from public/resume.pdf — replace that file, keep the name

  // Tech skills — mirrors the resume (HKUK.tex)
  skills: [
    // Core ML/LLM
    "Python",
    "PyTorch",
    "Hugging Face",
    "LangGraph",
    "RAG",
    "3D Gaussian Splatting",
    "Ollama",
    // Serving & data
    "FastAPI",
    "PostgreSQL",
    "pgvector",
    "Qdrant",
    "LanceDB",
    "Redis",
    "SQL",
    // Infra & ops
    "Docker",
    "AWS",
    "GitHub Actions",
    "Prometheus",
    "Grafana",
    // Edge
    "Next.js",
    "TypeScript",
  ],

  // Spoken languages — your polyglot edge (display order matters)
  languages: [
    { name: "English",   level: "Fluent" },
    { name: "Spanish",   level: "Fluent" },
    { name: "Mandarin",  level: "Conversational" },
    { name: "Hindi",     level: "Native" },
    { name: "Marathi",   level: "Native" },
    { name: "Japanese",  level: "Basic" },
    { name: "German",    level: "Basic" },
    { name: "Norwegian", level: "Basic" },
    // Reads only: Korean, Russian, Arabic script
    // Understands: Italian, Portuguese (via Spanish)
  ],
};
