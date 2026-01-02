// Debug script to check authentication and API connectivity
async function debugApiConnection() {
  console.log('=== API Connection Debug ===');
  
  // Check if we're in browser environment
  if (typeof window === 'undefined') {
    console.log('This script must run in a browser environment');
    return;
  }
  
  // Check if user is authenticated
  const sessionStr = localStorage.getItem('auth_session');
  if (!sessionStr) {
    console.log('❌ No authentication session found in localStorage');
    console.log('Please sign in first');
    return;
  }
  
  try {
    const session = JSON.parse(sessionStr);
    console.log('✅ Authentication session found:');
    console.log('- User ID:', session.user.id);
    console.log('- Token present:', !!session.token);
    console.log('- Token length:', session.token.length);
    
    // Check if token is valid (not expired)
    const tokenParts = session.token.split('.');
    if (tokenParts.length === 3) {
      try {
        const payload = JSON.parse(atob(tokenParts[1]));
        const now = Math.floor(Date.now() / 1000);
        const exp = payload.exp;
        
        if (exp < now) {
          console.log('❌ Token is expired');
          console.log('- Token expired at:', new Date(exp * 1000).toISOString());
          console.log('- Current time:', new Date(now * 1000).toISOString());
          return;
        } else {
          console.log('✅ Token is not expired');
          console.log('- Token expires at:', new Date(exp * 1000).toISOString());
        }
      } catch (e) {
        console.log('⚠️ Could not decode token payload:', e.message);
      }
    }
    
    // Test API connection
    console.log('\n=== Testing API Connection ===');
    
    const API_BASE_URL = 'http://localhost:8000/api';
    
    // Test health check (no auth required)
    try {
      const healthResponse = await fetch(`${API_BASE_URL}/health`);
      const healthData = await healthResponse.json();
      console.log('✅ Health check:', healthData);
    } catch (e) {
      console.log('❌ Health check failed:', e.message);
      return;
    }
    
    // Test authenticated request
    try {
      const tasksResponse = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (tasksResponse.status === 401) {
        console.log('❌ Authentication failed - token rejected by server');
        const errorData = await tasksResponse.json();
        console.log('Server error:', errorData);
        return;
      }
      
      if (tasksResponse.status === 200) {
        const tasksData = await tasksResponse.json();
        console.log('✅ Successfully fetched tasks');
        console.log('- Number of tasks:', tasksData.data?.length || 0);
        console.log('- Task data:', tasksData);
        
        // Show available task IDs if any exist
        if (tasksData.data && tasksData.data.length > 0) {
          console.log('- Available task IDs:');
          tasksData.data.forEach((task, index) => {
            console.log(`  ${index + 1}. ${task.id} - ${task.title}`);
          });
        }
      } else {
        console.log('❌ Tasks request failed:', tasksResponse.status);
        const errorData = await tasksResponse.json();
        console.log('Server error:', errorData);
      }
    } catch (e) {
      console.log('❌ Tasks request failed with network error:', e.message);
    }
    
    // Test the specific task ID that's failing
    const problematicTaskId = '4a8ffeed-f135-449b-861b-b5c8913e48a8';
    console.log(`\n=== Testing specific task ID: ${problematicTaskId} ===`);
    
    try {
      const taskResponse = await fetch(`${API_BASE_URL}/tasks/${problematicTaskId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (taskResponse.status === 404) {
        console.log('❌ Task not found - this explains the error');
        console.log('The task ID does not exist in the database');
      } else if (taskResponse.status === 403) {
        console.log('❌ Access denied - this task belongs to a different user');
        console.log('User isolation is working correctly');
      } else if (taskResponse.status === 200) {
        const taskData = await taskResponse.json();
        console.log('✅ Task found:', taskData);
      } else {
        console.log(`❌ Unexpected response: ${taskResponse.status}`);
        const errorData = await taskResponse.json();
        console.log('Server error:', errorData);
      }
    } catch (e) {
      console.log('❌ Task request failed with network error:', e.message);
    }
    
  } catch (e) {
    console.log('❌ Error parsing session:', e.message);
  }
}

// Run the debug function
debugApiConnection().catch(console.error);