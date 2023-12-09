import axios from "axios";
import fs from 'fs'

// Replace 'YOUR_API_KEY' with your actual OpenAI API key
const apiKey = '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';
let assistantId;
let threadId;
let runId;

// Step 1: Create an Assistant
async function createAssistant() {
  try {
    const response = await axios.post('https://api.openai.com/v1/assistants', {
      instructions: "You are a personal Python tutor.  python questions. with code example",
      name: "Python Tutor",
      tools: [{ type: "code_interpreter" }],
      model: "gpt-4",
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'OpenAI-Beta': 'assistants=v1',
      },
    });

    assistantId = response.data.id;
    console.log(`Assistant created with ID: ${assistantId}`);
  } catch (error) {
    console.error('Error creating assistant:', error.response ? error.response.data : error.message);
  }
}

// Step 2: Create a Thread
async function createThread() {
  try {
    const response = await axios.post('https://api.openai.com/v1/threads', {}, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'OpenAI-Beta': 'assistants=v1',
      },
    });

    threadId = response.data.id;
    console.log(`Thread created with ID: ${threadId}`);
  } catch (error) {
    console.error('Error creating thread:', error.response ? error.response.data : error.message);
  }
}

// Step 3: Add Messages to the Thread
async function addMessage() {
  try {
    await axios.post(`https://api.openai.com/v1/threads/${threadId}/messages`, {
      role: 'user',
      content: 'how to concatenate two strings, give code example',
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'OpenAI-Beta': 'assistants=v1',
      },
    });

    console.log('Message added to the thread.');
  } catch (error) {
    console.error('Error adding message:', error.response ? error.response.data : error.message);
  }
}

// Step 4: Run the Assistant on the Thread
async function runAssistant() {
  try {
    const response = await axios.post(`https://api.openai.com/v1/threads/${threadId}/runs`, {
      assistant_id: assistantId,
      instructions: "Please address the user as Jane Doe. The user has a premium account.",
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'OpenAI-Beta': 'assistants=v1',
      },
    });

    runId = response.data.id;
    console.log(`Assistant run initiated with ID: ${runId}`);
  } catch (error) {
    console.error('Error running assistant:', error.response ? error.response.data : error.message);
  }
}

// Step 5: Wait for Run Completion
async function waitForRunCompletion() {
  let status = 'queued';
  while (status === 'queued' || status === 'in_progress') {
    try {
      const response = await axios.get(`https://api.openai.com/v1/threads/${threadId}/runs/${runId}`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'OpenAI-Beta': 'assistants=v1',
        },
      });
      status = response.data.status;
      console.log('Run status:', status);
    } catch (error) {
      console.error('Error checking run status:', error.response ? error.response.data : error.message);
      break;
    }
    // Wait for a short period before checking the status again
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
}

// Step 6: Display the Assistant Response
async function displayAssistantResponse() {
  try {
    const response = await axios.get(`https://api.openai.com/v1/threads/${threadId}/messages`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'OpenAI-Beta': 'assistants=v1',
      },
    });

    // const assistantResponse = response.data.messages.find(message => message.role === 'assistant');
    const responseData = response.data;
    if (responseData) {
      console.log('assistant response : ', responseData.data[0].content)
    }
  } catch (error) {
    console.error('Error displaying assistant response:', error.response ? error.response.data : error.message);
  }
}

// Example Usage:
async function main() {
  await createAssistant();
  await createThread();
  await addMessage();
  await runAssistant();
  await waitForRunCompletion();
  await displayAssistantResponse();
}

main();
