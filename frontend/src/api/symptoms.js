import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_URL || "";

/**
 * Sends user symptom text to the backend for analysis.
 *
 * @param {string} text - The user's symptom description.
 * @returns {Promise<Object>} The full response data object containing:
 *   - is_emergency: boolean
 *   - emergency_message: string | null
 *   - conditions: Array<{ name: string, explanation: string, severity: string, source: string }>
 *   - disclaimer: string
 * @throws {Error} With a clean user-facing message on failure.
 */
export default async function fetchSymptomAnalysis(text) {
  try {
    const response = await axios.post(`${BASE_URL}/api/symptoms`, { text });
    return response.data;
  } catch (error) {
    if (error.response) {
      if (error.response.status === 429) {
        throw new Error(
          "Too many requests. Please wait a moment before trying again."
        );
      }
      if (error.response.status === 500) {
        throw new Error(
          "Something went wrong on our end. Please try again shortly."
        );
      }
    }
    throw new Error(
      "Unable to reach the server. Please check your connection and try again."
    );
  }
}
