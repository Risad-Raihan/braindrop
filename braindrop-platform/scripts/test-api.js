/**
 * Simple script to test the Physics RAG API connection
 * Run with: node scripts/test-api.js
 */

const API_URL = 'http://localhost:8000';

async function testApiConnection() {
  console.log('🔍 Testing Physics RAG API connection...\n');

  try {
    // Test health endpoint
    console.log('1. Testing health endpoint...');
    const healthResponse = await fetch(`${API_URL}/health`);
    
    if (healthResponse.ok) {
      const health = await healthResponse.json();
      console.log('✅ Health check passed');
      console.log(`   Status: ${health.status}`);
      console.log(`   Services: ${Object.entries(health.services).map(([k, v]) => `${k}=${v}`).join(', ')}`);
    } else {
      console.log('❌ Health check failed');
      console.log(`   Status: ${healthResponse.status}`);
    }

    console.log('\n2. Testing chat endpoint...');
    
    // Test chat endpoint
    const chatResponse = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: "What is Newton's first law?",
        include_sources: true,
        search_type: 'hybrid',
        top_k: 3
      })
    });

    if (chatResponse.ok) {
      const chat = await chatResponse.json();
      console.log('✅ Chat endpoint working');
      console.log(`   Response length: ${chat.response.length} characters`);
      console.log(`   Sources found: ${chat.sources ? chat.sources.length : 0}`);
      console.log(`   Search time: ${chat.search_time || 'N/A'}s`);
      console.log(`   Generation time: ${chat.generation_time || 'N/A'}s`);
    } else {
      console.log('❌ Chat endpoint failed');
      console.log(`   Status: ${chatResponse.status}`);
      const error = await chatResponse.text();
      console.log(`   Error: ${error}`);
    }

  } catch (error) {
    console.log('❌ Connection failed');
    console.log(`   Error: ${error.message}`);
    console.log('\n💡 Make sure the Physics RAG backend is running on http://localhost:8000');
    console.log('   From the physics_rag_weaviate directory, run: python run_server.py');
  }

  console.log('\n🏁 API test completed');
}

// Run the test
testApiConnection();

