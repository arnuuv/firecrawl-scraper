import React, { useState } from "react";

const actions = [
  { label: "Craft", icon: "✏️" },
  { label: "Analyze", icon: "📊" },
  { label: "Research", icon: "🔎" },
  { label: "Code", icon: "💻" },
  { label: "Playbook", icon: "📄", external: true },
];

export default function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      setResponse(`Atreides is working on: "${input}" ...`);
    } else {
      setResponse("");
    }
  };

  return (
    <div className="min-h-screen bg-[#fafaf8] flex flex-col">
      {/* Navbar */}
      <nav className="w-full flex items-center justify-between px-8 py-4 bg-[#fafaf8]">
        <div className="flex items-center gap-3">
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/4/4e/House_Atreides_symbol.png"
            alt="Atreides Logo"
            className="h-8 w-8"
          />
          <span className="text-2xl font-bold tracking-tight text-gray-800 font-serif">
            atreides
          </span>
        </div>
        <div className="flex gap-8 text-gray-700 font-medium">
          <a href="#" className="hover:text-blue-600">Intro</a>
          <a href="#" className="hover:text-blue-600">Use cases</a>
          <a href="#" className="hover:text-blue-600">Community</a>
          <a href="#" className="hover:text-blue-600">Benchmarks</a>
        </div>
        <div className="flex gap-2">
          <button className="px-5 py-1 rounded-lg border border-black text-black font-semibold hover:bg-gray-100 transition">Sign in</button>
          <button className="px-5 py-1 rounded-lg border border-gray-300 bg-white text-black font-semibold hover:bg-gray-100 transition">Sign up</button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center">
        <div className="w-full max-w-3xl flex flex-col items-center mt-12">
          <h1 className="text-4xl md:text-5xl font-serif font-semibold text-gray-800 mb-8 text-center">
            What can I do for you?
          </h1>
          <form
            onSubmit={handleSubmit}
            className="w-full flex flex-col items-center"
          >
            <div className="w-full flex items-center bg-white rounded-2xl shadow-lg px-6 py-4 gap-2 border border-gray-200 focus-within:border-blue-500 transition-all"
                 style={{ minWidth: 500, maxWidth: 700 }}>
              <button type="button" title="Edit" className="text-gray-400 hover:text-blue-500 p-2">
                <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M15.232 5.232l3.536 3.536M9 13l6.586-6.586a2 2 0 112.828 2.828L11.828 15.828a4 4 0 01-2.828 1.172H7v-2a4 4 0 011.172-2.828z"></path></svg>
              </button>
              <button type="button" title="Language" className="text-gray-400 hover:text-blue-500 p-2">
                <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 6v6l4 2"></path></svg>
              </button>
              <button type="button" title="Attach" className="text-gray-400 hover:text-blue-500 p-2">
                <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.586-6.586a4 4 0 10-5.656-5.656l-6.586 6.586"></path></svg>
              </button>
              <input
                type="text"
                placeholder="Give Atreides a task to work on..."
                className="flex-1 bg-transparent outline-none text-lg px-2"
                autoComplete="off"
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <button
                type="submit"
                className="ml-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold px-5 py-2 rounded-xl border border-gray-300 shadow transition-all"
              >
                <span className="flex items-center gap-2">
                  <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"></path></svg>
                  Create
                </span>
              </button>
            </div>
          </form>
          {/* Action Chips */}
          <div className="flex flex-wrap gap-3 mt-6">
            {actions.map((action) => (
              <button
                key={action.label}
                className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium border border-gray-200 transition"
                onClick={() => setInput(action.label)}
              >
                <span>{action.icon}</span>
                {action.label}
                {action.external && (
                  <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M14 3h7v7M10 14L21 3M21 21H3V3"></path></svg>
                )}
              </button>
            ))}
          </div>
          {/* Response */}
          <div className="w-full mt-8 text-center text-lg text-gray-600">
            {response}
          </div>
        </div>
      </main>
    </div>
  );
}
