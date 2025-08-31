#!/usr/bin/env node

/**
 * Debug script to test the clinics API transformation
 * Run this in the browser console after logging in
 */

// Test 1: Check raw API response
async function testRawAPI() {
  console.log('=== TEST 1: Raw API Response ===');
  
  const token = localStorage.getItem('picobrain_access_token');
  if (!token) {
    console.error('❌ No token found. Please login first.');
    return;
  }
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/clinics', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    console.log('Raw API response:', data);
    console.log('Response type:', Array.isArray(data) ? 'Array' : typeof data);
    console.log('Response length:', data.length);
    
    return data;
  } catch (error) {
    console.error('❌ Error fetching raw API:', error);
  }
}

// Test 2: Check the transformed response from clinicsApi.list
async function testTransformedAPI() {
  console.log('\n=== TEST 2: Transformed API Response ===');
  
  // This needs to be run in the context of the React app
  // Check if clinicsApi is available
  if (typeof window !== 'undefined' && window.clinicsApi) {
    try {
      const result = await window.clinicsApi.list();
      console.log('Transformed response:', result);
      console.log('Has items?', 'items' in result);
      console.log('Has total?', 'total' in result);
      console.log('Items type:', Array.isArray(result.items) ? 'Array' : typeof result.items);
      console.log('Items length:', result.items?.length);
      console.log('Total value:', result.total);
      
      return result;
    } catch (error) {
      console.error('❌ Error with transformed API:', error);
    }
  } else {
    console.log('⚠️ clinicsApi not found in window. Try importing it first.');
    console.log('Run this in the browser console:');
    console.log(`
import { clinicsApi } from '/src/lib/api/endpoints/clinics';
window.clinicsApi = clinicsApi;
    `);
  }
}

// Test 3: Check React Query cache
async function testReactQueryCache() {
  console.log('\n=== TEST 3: React Query Cache ===');
  
  // Check if React Query devtools are available
  if (typeof window !== 'undefined' && window.__REACT_QUERY_DEVTOOLS_GLOBAL_STORE__) {
    const queryClient = window.__REACT_QUERY_DEVTOOLS_GLOBAL_STORE__.queryClient;
    const queries = queryClient.getQueryCache().getAll();
    
    const clinicQueries = queries.filter(q => 
      q.queryKey.some(k => k === 'clinics' || (typeof k === 'string' && k.includes('clinic')))
    );
    
    console.log('Found clinic queries:', clinicQueries.length);
    
    clinicQueries.forEach((query, index) => {
      console.log(`Query ${index + 1}:`, {
        key: query.queryKey,
        state: query.state.status,
        data: query.state.data,
        error: query.state.error
      });
    });
  } else {
    console.log('⚠️ React Query DevTools not found.');
    console.log('Make sure React Query DevTools are installed.');
  }
}

// Run all tests
async function runAllTests() {
  console.log('🔍 Starting Clinics Frontend Debug...\n');
  
  await testRawAPI();
  await testTransformedAPI();
  await testReactQueryCache();
  
  console.log('\n✅ Debug complete. Check the results above.');
}

// Instructions
console.log(`
📋 INSTRUCTIONS:
1. Open the browser with your React app
2. Login to the application
3. Navigate to the Clinics page
4. Open browser DevTools Console (F12)
5. Copy and paste this entire script
6. Call: runAllTests()

Or run individual tests:
- testRawAPI() - Check raw backend response
- testTransformedAPI() - Check transformed response
- testReactQueryCache() - Check React Query cache
`);

// Export for browser
if (typeof window !== 'undefined') {
  window.debugClinics = {
    testRawAPI,
    testTransformedAPI,
    testReactQueryCache,
    runAllTests
  };
  console.log('✅ Debug functions loaded. Access them via window.debugClinics');
}
