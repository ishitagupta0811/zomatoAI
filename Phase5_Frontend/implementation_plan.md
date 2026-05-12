# Phase 5 Frontend UI Implementation Plan

This plan details the process for building the "Zomato AI" web application interface using Next.js, React, and Tailwind CSS, as outlined in our architecture document.

## Goal Description

We will build a visually stunning, modern web interface that allows users to interact with our backend API and Groq LLM. The frontend will feature a dynamic gradient background, glassmorphism UI elements, and real-time loading states while the AI processes the recommendations.

## Proposed Changes

### 1. Update Architecture Document
#### [MODIFY] [phase-wise architecture.md](file:///c:/Users/ishit/OneDrive/Documents/Product%20Management-ISHITA/Project/zomatoAI/phase-wise%20architecture.md)
- Remove the note stating that Phase 5 is deferred to a future milestone.

### 2. Initialize Next.js Project
- Run the `create-next-app` command in the project root to generate a new `frontend` directory:
  `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --yes`

### 3. Implement Global Design System (Tailwind)
#### [MODIFY] `frontend/src/app/globals.css`
- Apply a vibrant, animated mesh gradient background.
- Define custom utility classes for "glassmorphism" (translucent white panels with blur) and subtle micro-animations (hover lifts, fade-ins).

### 4. Build Components
#### [NEW] `frontend/src/components/RestaurantCard.tsx`
- A premium card component displaying the restaurant's name, rating, cost, and a distinct, visually highlighted section for the `ai_explanation`.
#### [NEW] `frontend/src/components/LoadingState.tsx`
- A skeleton loader or animated "AI is thinking..." visual indicator to display while waiting for the Groq API.

### 5. Main Application Logic
#### [MODIFY] `frontend/src/app/page.tsx`
- **State Management:** Use `useState` and `useEffect` to manage form inputs and fetch dropdown data (locations/cuisines) from the FastAPI backend.
- **Hero Section:** Display an eye-catching title ("Zomato AI") and brief description.
- **Filter Form:** Build a glassmorphic form with:
  - Dropdowns for Location and Cuisine.
  - Number inputs/sliders for Budget and Rating.
  - A text area for the `additional_context` prompt.
- **API Integration:** Submit the form data to `http://localhost:8000/api/v1/recommend` and render the results.

## Open Questions

> [!WARNING]
> Before I proceed, do you have any specific color palette preferences for the modern design (e.g., warm sunset orange/pink, cool ocean blue/purple, or sleek dark mode)? If you don't have a preference, I will implement a premium warm gradient. 

## Verification Plan

### Automated Tests
- I will run both the FastAPI server (`backend/main.py`) and the Next.js development server (`npm run dev`) simultaneously.
- I will use a browser subagent to interact with the UI, submit a test search, and verify that the AI-recommended restaurants populate on the screen correctly.
