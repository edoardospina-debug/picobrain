/**
 * Simple browser console test for clinics data flow
 * Copy and paste this entire code block into the browser console
 */

// Test the API directly
async function testClinicsFlow() {
  console.log('🔍 Testing Clinics Data Flow...\n');
  
  // Step 1: Check token
  const token = localStorage.getItem('picobrain_access_token');
  if (!token) {
    console.error('❌ No token found. Please login first.');
    return;
  }
  console.log('✅ Token found');
  
  // Step 2: Test raw API call
  console.log('\n📡 Testing raw API call...');
  try {
    const rawResponse = await fetch('http://localhost:8000/api/v1/clinics', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const rawData = await rawResponse.json();
    console.log('Raw API response:', rawData);
    console.log('Is Array?', Array.isArray(rawData));
    console.log('Length:', rawData?.length);
    console.log('First item:', rawData?.[0]);
    
    // Step 3: Test what DataTable expects
    console.log('\n📊 What DataTable expects:');
    const expectedFormat = {
      items: rawData,
      total: rawData.length
    };
    console.log('Expected format:', expectedFormat);
    
    // Step 4: Test with axios (mimicking the api client)
    console.log('\n🔧 Testing with axios (if available)...');
    if (typeof axios !== 'undefined') {
      const axiosResponse = await axios.get('http://localhost:8000/api/v1/clinics', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      console.log('Axios response object:', axiosResponse);
      console.log('Axios response.data:', axiosResponse.data);
      console.log('Is response.data an Array?', Array.isArray(axiosResponse.data));
    } else {
      console.log('⚠️ Axios not available in global scope');
    }
    
    // Step 5: Check React Query cache
    console.log('\n🗃️ Checking React Query cache...');
    const queryKeys = ['clinics'];
    
    // Try to find React Query's queryClient
    let queryClient = null;
    
    // Method 1: Check for devtools
    if (window.__REACT_QUERY_DEVTOOLS_GLOBAL_STORE__) {
      queryClient = window.__REACT_QUERY_DEVTOOLS_GLOBAL_STORE__.queryClient;
      console.log('Found queryClient via devtools');
    }
    
    // Method 2: Check React fiber tree (NextJS specific)
    if (!queryClient && window._reactRootContainer) {
      console.log('Searching React fiber tree...');
      // This is more complex and might not work in all cases
    }
    
    if (queryClient) {
      const cache = queryClient.getQueryCache();
      const queries = cache.getAll();
      const clinicQueries = queries.filter(q => 
        JSON.stringify(q.queryKey).includes('clinics')
      );
      
      console.log(`Found ${clinicQueries.length} clinic-related queries`);
      clinicQueries.forEach((q, i) => {
        console.log(`Query ${i + 1}:`, {
          key: q.queryKey,
          status: q.state.status,
          dataType: Array.isArray(q.state.data) ? 'Array' : typeof q.state.data,
          data: q.state.data
        });
      });
    } else {
      console.log('⚠️ Could not find queryClient. Try navigating to /clinics page first.');
    }
    
    console.log('\n✅ Test complete. Check the results above.');
    console.log('🔍 Look for:');
    console.log('  1. Is the raw API returning an array?');
    console.log('  2. Does the transformation to {items, total} look correct?');
    console.log('  3. What does React Query cache show?');
    
  } catch (error) {
    console.error('❌ Error during test:', error);
  }
}

// Auto-run
testClinicsFlow();
