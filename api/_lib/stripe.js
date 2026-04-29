import Stripe from "stripe";
import { requireEnv } from "./config.js";

let client = null;

export function getStripe() {
  if (client) return client;
  client = new Stripe(requireEnv("STRIPE_SECRET_KEY"));
  return client;
}
