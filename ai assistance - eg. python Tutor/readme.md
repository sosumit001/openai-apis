# Python Tutor Assistant API Integration

## Overview

This project demonstrates the integration of the OpenAI Assistant API to create a Python Tutor assistant. The assistant supports Python-related queries, utilizing the Code Interpreter tool.

[![Alt Text](https://img.youtube.com/vi/pPXRmQ37M6k?si/0.jpg)](https://www.youtube.com/watch?v=pPXRmQ37M6k?si)

## Integration Steps

| Step | Method | Endpoint |
|------|--------|----------|
| 1.   | `createAssistant()` | `POST /v1/assistants` |
| 2.   | `createThread()` | `POST /v1/threads` |
| 3.   | `addMessage()` | `POST /v1/threads/{threadId}/messages` |
| 4.   | `runAssistant()` | `POST /v1/threads/{threadId}/runs` |
| 5.   | `waitForRunCompletion()` | `GET /v1/threads/{threadId}/runs/{runId}` |
| 6.   | `displayAssistantResponse()` | `GET /v1/threads/{threadId}/messages` |

## Usage

To run the integration, follow these steps:

1. Create an assistant using `createAssistant()`.
2. Initiate a thread with `createThread()`.
3. Add a user message using `addMessage()` with the desired Python-related query.
4. Run the assistant on the thread using `runAssistant()`.
5. Wait for the run to complete with `waitForRunCompletion()`.
6. Display the assistant's response using `displayAssistantResponse()`.

Make sure to replace `{threadId}` and `{runId}` with the actual IDs obtained during the process.

## Setup

1. Install the required packages: `npm install`.
2. Set your OpenAI API key in the `apiKey` variable within the script.

## Example

```javascript
const main = async () => {
  await createAssistant();
  await createThread();
  await addMessage();
  await runAssistant();
  await waitForRunCompletion();
  await displayAssistantResponse();
};

main();
