export const profile = {
  name: "Hitendra Kawale",
  // Chinese name, carried over from the personal archive site. 高 is the "tall" gao.
  nameHan: "高泽贤",
  namePinyin: "Gāo Zéxián",
  initials: "HK",
  title: "AI Engineer",
  bio: "AI engineer building LLM systems, RAG pipelines, and 3D vision tools.",
  availability: "Open to AI roles and freelance work",

  // Short form for social cards, which truncate around 150 characters.
  cardBio:
    "AI engineer building LLM systems, RAG pipelines, and 3D vision tools. MSc Artificial Intelligence, University of Surrey.",

  // Links
  archive: "https://hitendra-chronicle.vercel.app",
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
