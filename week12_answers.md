# Week 12 Answers

## Exercise 1

**1. The messages the customer typed:**

I want to change my shipping address.
It's order A102.
9 Pine Street, Tampa.

**2. How many tool requests were refused, and why?**

Two tool requests were refused. The first was refused because the model tried using an order ID the customer had not provided. The second was refused because the model tried using a shipping address that the customer had not provided.

**3. If the customer now types "thanks", how many messages does Ollama receive on the next call?**

Ollama receives 11 messages: the system instructions, the 9 messages already in the conversation history, and the new user message saying "thanks."

**4. Why does "Do you sell gift cards?" still go to a person, and why is that acceptable?**

The chatbot checks for the handoff word "card," which also appears within "cards," so it sends the question to a human. This is acceptable because the chatbot is designed to be cautious about payment-related questions, even if it occasionally sends an unnecessary request to a person.

## Exercise 3
Customer Message:
I want to change my shipping address

Chatbot:
Sunny: Sure thing! To change your shipping address, I’ll need a fewdetails:

1. **Your order ID** – the unique identifier for the order you wantto update.
2. **The new shipping address** – full street address, city, state/province, and ZIP/postal code.

Once you provide those, I can submit a request to our staff for approval. Let me know!

Staff review: 
Not available, the chatbot asked me to provide an order ID and new shipping addresss

What I learned: 
Even with the guardrail off the AI might still ask for the correct information. However, the guardrail is important because it prevents the AI from submitting made-up information.

