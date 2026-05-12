"use client";

import { useState, useEffect } from "react";

interface Restaurant {
  name: string;
  location: string;
  rating: number;
  cost_for_two: number;
  cuisines: string;
  url: string | null;
  ai_explanation: string;
}

export default function Home() {
  const [locations, setLocations] = useState<string[]>([]);
  const [cuisines, setCuisines] = useState<string[]>([]);
  
  // Form State
  const [selectedLocation, setSelectedLocation] = useState("");
  const [selectedCuisine, setSelectedCuisine] = useState("");
  const [budget, setBudget] = useState(1500);
  const [minRating, setMinRating] = useState(4.0);
  const [context, setContext] = useState(""); // The top conversational bar
  
  // Result State
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Restaurant[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState("");

  // Fetch initial data
  useEffect(() => {
    fetch("https://zomatoai-saprrfuhjdbny4zlzpmahe.streamlit.app/api/v1/locations")
      .then((res) => res.json())
      .then((data) => {
        setLocations(data.locations || []);
        if (data.locations && data.locations.length > 0) setSelectedLocation(data.locations[0]);
      })
      .catch((err) => console.error("Error fetching locations:", err));

    fetch("https://zomatoai-saprrfuhjdbny4zlzpmahe.streamlit.app/api/v1/cuisines")
      .then((res) => res.json())
      .then((data) => {
        setCuisines(data.cuisines || []);
        if (data.cuisines && data.cuisines.length > 0) setSelectedCuisine(data.cuisines[0]);
      })
      .catch((err) => console.error("Error fetching cuisines:", err));
  }, []);

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError("");
    setHasSearched(true);
    setResults([]);

    try {
      const response = await fetch("https://zomatoai-saprrfuhjdbny4zlzpmahe.streamlit.app/api/v1/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          location: selectedLocation,
          budget_max: budget,
          cuisine_preference: selectedCuisine,
          min_rating: minRating,
          additional_context: context,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Something went wrong.");
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const setCravings = (craving: string) => {
    setContext(craving);
  };

  return (
    <div className="min-h-screen bg-[#f4f5f7] flex flex-col">
      {/* 1. Navbar */}
      <nav className="bg-white border-b border-gray-200 py-3 px-6 md:px-12 flex items-center justify-between z-10 sticky top-0">
        <div className="flex items-center gap-2">
          <span className="text-3xl font-black italic tracking-tighter zomato-red">zomato</span>
          <span className="text-xl font-medium text-gray-500 ml-2 mt-1">Zomato AI</span>
        </div>
        <div className="hidden md:flex gap-6 text-sm font-semibold text-gray-600 items-center">
          <a href="#" className="zomato-red border-b-2 border-[#e23744] pb-1">Home</a>
          <a href="#" className="hover:text-black transition">Dining Out</a>
          <a href="#" className="hover:text-black transition">Delivery</a>
          <a href="#" className="hover:text-black transition">Profile</a>
        </div>
      </nav>

      {/* 2. Hero Section with Search Card */}
      <section className="relative hero-gradient pt-16 pb-24 px-4 flex items-center justify-center">
        {/* Simulating the food background images with generic decorative shapes since we don't have images */}
        <div className="absolute inset-0 overflow-hidden opacity-20 pointer-events-none">
           <div className="absolute top-10 left-10 w-64 h-64 bg-black rounded-full mix-blend-overlay"></div>
           <div className="absolute bottom-10 right-10 w-80 h-80 bg-black rounded-full mix-blend-overlay"></div>
        </div>

        {/* The White Search Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full z-10 animate-fade-in relative">
          <h1 className="text-2xl font-bold text-center text-gray-900 mb-6">
            Find Your Perfect Meal with Zomato AI
          </h1>

          {/* Conversational Bar */}
          <div className="relative mb-4">
            <input 
              type="text" 
              placeholder="Hi! What are you craving today?" 
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-full py-3 px-5 pr-28 focus:outline-none focus:ring-2 focus:ring-[#e23744]/50 focus:border-[#e23744] transition-all"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
            />
            <button 
              onClick={() => handleSubmit()}
              className="absolute right-2 top-2 bg-zomato-red hover-bg-zomato-red text-white text-sm font-bold py-1.5 px-4 rounded-full transition-colors"
            >
              Send
            </button>
            <div className="absolute right-24 top-3 text-red-500">
               {/* Microphone Icon Placeholder */}
               <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8h-2a5 5 0 01-10 0H3a7.001 7.001 0 006 6.93V17H6v2h8v-2h-3v-2.07z" clipRule="evenodd" />
                </svg>
            </div>
          </div>

          {/* Quick Pill Buttons */}
          <div className="flex justify-center gap-3 mb-6">
            <button type="button" onClick={() => setCravings("Italian")} className="pill-btn">Italian</button>
            <button type="button" onClick={() => setCravings("Spicy")} className="pill-btn">Spicy</button>
            <button type="button" onClick={() => setCravings("Dessert")} className="pill-btn">Dessert</button>
            <button type="button" onClick={() => setSelectedLocation("Near Me")} className="pill-btn">Near Me</button>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Location Input */}
              <div>
                <label className="block text-xs font-semibold text-gray-500 mb-1">Location</label>
                <select 
                  className="w-full bg-white border border-gray-200 text-gray-800 rounded-lg py-2.5 px-3 focus:outline-none focus:border-gray-400"
                  value={selectedLocation} 
                  onChange={(e) => setSelectedLocation(e.target.value)}
                  required
                >
                  <option value="Near Me">Near Me</option>
                  {locations.map((loc) => (
                    <option key={loc} value={loc}>{loc}</option>
                  ))}
                </select>
              </div>

              {/* Cuisine Input */}
              <div>
                <label className="block text-xs font-semibold text-gray-500 mb-1">Cuisine</label>
                <select 
                  className="w-full bg-white border border-gray-200 text-gray-800 rounded-lg py-2.5 px-3 focus:outline-none focus:border-gray-400"
                  value={selectedCuisine} 
                  onChange={(e) => setSelectedCuisine(e.target.value)}
                  required
                >
                  {cuisines.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              {/* Budget Input */}
              <div>
                <label className="block text-xs font-semibold text-gray-500 mb-1">Budget</label>
                <input 
                  type="number" min="100" max="10000" step="100" 
                  value={budget} onChange={(e) => setBudget(Number(e.target.value))}
                  placeholder="e.g., ₹500-₹1000"
                  className="w-full bg-white border border-gray-200 text-gray-800 rounded-lg py-2.5 px-3 focus:outline-none focus:border-gray-400"
                />
              </div>

              {/* Min Rating Input (Mapped to "Specific Cravings" space in UI mock) */}
              <div>
                <label className="block text-xs font-semibold text-gray-500 mb-1">Min Rating</label>
                <select 
                  value={minRating} onChange={(e) => setMinRating(Number(e.target.value))}
                  className="w-full bg-white border border-gray-200 text-gray-800 rounded-lg py-2.5 px-3 focus:outline-none focus:border-gray-400"
                >
                  <option value={3.0}>3.0+ Stars</option>
                  <option value={3.5}>3.5+ Stars</option>
                  <option value={4.0}>4.0+ Stars</option>
                  <option value={4.5}>4.5+ Stars</option>
                </select>
              </div>
            </div>

            {/* Red Submit Button */}
            <button 
              type="submit" 
              disabled={loading}
              className="mt-2 w-full py-3 bg-zomato-red hover-bg-zomato-red text-white font-bold rounded-lg transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? "Analyzing Cravings..." : "Get Recommendations"}
            </button>
          </form>
        </div>
      </section>

      {/* 3. Results Section */}
      <section className="flex-1 max-w-5xl w-full mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-8">
          Personalized Picks for You
        </h2>

        {loading && (
          <div className="flex flex-col items-center justify-center py-20 animate-pulse">
            <div className="w-12 h-12 border-4 border-[#e23744] border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-gray-500 font-medium">Finding the best matches...</p>
          </div>
        )}

        {!loading && error && (
          <div className="bg-red-50 border border-red-200 p-6 rounded-xl text-center">
            <p className="text-red-600 font-medium">{error}</p>
          </div>
        )}

        {!loading && !error && hasSearched && results.length === 0 && (
          <div className="bg-white border border-gray-200 p-12 rounded-xl text-center">
            <p className="text-gray-600 font-medium">No restaurants found. Try exploring other locations or cuisines!</p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {results.map((r, idx) => (
              <div key={idx} className="bg-white border border-gray-100 rounded-xl shadow-sm hover-lift flex overflow-hidden animate-fade-in" style={{ animationDelay: `${idx * 0.1}s` }}>
                
                {/* Food Image Placeholder */}
                <div className="w-32 bg-gray-200 shrink-0 relative flex items-center justify-center border-r border-gray-100">
                   <span className="text-4xl">🍲</span>
                </div>

                {/* Card Details */}
                <div className="p-4 flex-1 flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start mb-1">
                      <h3 className="text-lg font-bold text-gray-900 leading-tight">{r.name}</h3>
                      <div className="flex items-center gap-1 bg-green-50 px-1.5 py-0.5 rounded text-green-700 text-xs font-bold">
                        <span>★</span> {r.rating}
                      </div>
                    </div>
                    <p className="text-xs font-medium text-gray-500 mb-3">
                      {r.cuisines} • ₹{r.cost_for_two} for two
                    </p>
                  </div>
                  
                  {/* AI Reason Box */}
                  <div className="bg-[#fff0f1] text-[#b32b36] p-3 rounded-lg text-xs font-medium border border-[#ffe0e2]">
                    <span className="font-bold mr-1">AI Reason:</span> 
                    {r.ai_explanation.replace('\u20b9', 'Rs.')}
                  </div>
                </div>

              </div>
            ))}
          </div>
        )}
      </section>

      {/* 4. Footer */}
      <footer className="bg-white border-t border-gray-200 py-6 px-12 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
        <div>
          <span className="text-xl font-black italic tracking-tighter zomato-red">zomato</span>
          <p className="mt-1 text-xs">© 2026 Zomato AI. All rights reserved.</p>
        </div>
        <div className="flex items-center gap-4 mt-4 md:mt-0">
          <span className="font-semibold text-gray-700">Follow Us:</span>
          {/* Social Icons Placeholder */}
          <div className="flex gap-3 text-gray-400">
             <span className="hover:text-black cursor-pointer">FB</span>
             <span className="hover:text-black cursor-pointer">TW</span>
             <span className="hover:text-black cursor-pointer">IG</span>
             <span className="hover:text-black cursor-pointer">TK</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
