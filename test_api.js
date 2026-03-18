const fetch = require('node-fetch');

async function test() {
  console.log("Testing API...");
  try {
    const res = await fetch('http://localhost:3000/api/extract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ engine: 'x', target: 'elonmusk' })
    });
    const text = await res.text();
    console.log("STATUS:", res.status);
    console.log("RESPONSE:", text.substring(0, 500) + '...');
  } catch(e) {
    console.error(e);
  }
}

test();
