# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: uat_journey.spec.ts >> NyayaSetu Comprehensive UAT Journey >> Phase 10: Officer Processing
- Location: tests\uat_journey.spec.ts:117:7

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.click: Target page, context or browser has been closed
Call log:
  - waiting for getByText('Test Water Leakage in Area 51 1785484039874').first()

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - link "Skip to main content" [ref=e4] [cursor=pointer]:
    - /url: "#main-content"
  - banner [ref=e5]:
    - navigation "Main navigation" [ref=e10]:
      - link "NyayaSetu home" [ref=e11] [cursor=pointer]:
        - /url: /
        - generic [ref=e17]:
          - generic [ref=e18]: NYAYA SETU
          - generic [ref=e19]: Grievance Redressal Prototype
      - generic [ref=e20]:
        - list [ref=e21]:
          - listitem [ref=e22]:
            - link "Home" [ref=e23] [cursor=pointer]:
              - /url: /
          - listitem [ref=e24]:
            - link "Officer Dashboard" [ref=e25] [cursor=pointer]:
              - /url: /dashboard
          - listitem [ref=e31]:
            - link "Assigned Grievances" [active] [ref=e32] [cursor=pointer]:
              - /url: /complaints
        - generic [ref=e36]:
          - button "Switch to dark mode" [ref=e37] [cursor=pointer]
          - generic [ref=e40]:
            - generic [ref=e41]:
              - generic "devansh12" [ref=e45]: Devansh Officer
              - generic [ref=e46]: staff
            - button "Logout" [ref=e47] [cursor=pointer]
  - main [ref=e51]:
    - generic [ref=e52]:
      - generic [ref=e53]:
        - generic [ref=e54]:
          - heading "Welcome, Officer Devansh Officer" [level=2] [ref=e55]
          - paragraph [ref=e56]:
            - text: "Assigned App:"
            - strong [ref=e57]: electricity
            - text: redresses desk
        - button "Refresh Queue" [ref=e59] [cursor=pointer]
      - generic [ref=e65]:
        - generic [ref=e71]:
          - heading "0" [level=4] [ref=e72]
          - text: Assigned Cases
        - generic [ref=e78]:
          - heading "0" [level=4] [ref=e79]
          - text: Active Cases
        - generic [ref=e85]:
          - heading "0" [level=4] [ref=e86]
          - text: Resolved Cases
        - generic [ref=e91]:
          - heading "0" [level=4] [ref=e92]
          - text: SLA Breaches
      - generic [ref=e93]:
        - generic [ref=e94]:
          - heading "Department Geospatial Queue" [level=2] [ref=e99]
          - generic [ref=e100]: electricity Department Boundaries
        - region "Grievance locations map" [ref=e102]:
          - generic [ref=e103]:
            - generic:
              - generic [ref=e106]:
                - button "Zoom in" [ref=e107] [cursor=pointer]: +
                - button "Zoom out" [ref=e108] [cursor=pointer]: −
              - generic [ref=e109]:
                - link "Leaflet" [ref=e110] [cursor=pointer]:
                  - /url: https://leafletjs.com
                - text: "| ©"
                - link "OpenStreetMap" [ref=e115] [cursor=pointer]:
                  - /url: https://www.openstreetmap.org/copyright
                - text: contributors
      - generic [ref=e116]:
        - generic [ref=e117]:
          - heading "Grievance Backlog & Queue" [level=3] [ref=e118]
          - generic [ref=e119]:
            - textbox "Search by ID, title or address..." [ref=e121]
            - combobox [ref=e123] [cursor=pointer]:
              - option "All Statuses" [selected]
              - option "Pending"
              - option "In Progress"
              - option "Resolved"
              - option "Escalated"
              - option "Admin Failure"
            - generic [ref=e124] [cursor=pointer]:
              - checkbox "SLA Breached Only" [ref=e125]
              - generic [ref=e126]: SLA Breached Only
        - table [ref=e128]:
          - rowgroup [ref=e129]:
            - row [ref=e130]:
              - columnheader "Grievance ID" [ref=e131]
              - columnheader "Title & Date" [ref=e132]
              - columnheader "Location" [ref=e133]
              - columnheader "Urgency" [ref=e134]
              - columnheader "Deadline (SLA)" [ref=e135]
              - columnheader "Status" [ref=e136]
              - columnheader "Actions" [ref=e137]
          - rowgroup [ref=e138]:
            - row [ref=e139] [cursor=pointer]:
              - cell "#23" [ref=e140]
              - cell "Test Water Leakage in Area 51 1785475185667 Lodged on 7/31/2026" [ref=e141]:
                - generic [ref=e142]: Test Water Leakage in Area 51 1785475185667
                - generic [ref=e143]: Lodged on 7/31/2026
              - cell "Unknown," [ref=e147]:
                - generic "Area 51 Main Street" [ref=e148]: Unknown,
              - cell [ref=e149]
              - cell "8/2/2026 (Normal)" [ref=e151]
              - cell [ref=e153]
              - cell [ref=e155]:
                - button "Review" [ref=e156]
            - row [ref=e159] [cursor=pointer]:
              - cell "#22" [ref=e160]
              - cell "Test Water Leakage in Area 51 Lodged on 7/31/2026" [ref=e161]:
                - generic [ref=e162]: Test Water Leakage in Area 51
                - generic [ref=e163]: Lodged on 7/31/2026
              - cell "Unknown," [ref=e167]:
                - generic "Area 51 Main Street" [ref=e168]: Unknown,
              - cell [ref=e169]
              - cell "8/2/2026 (Normal)" [ref=e171]
              - cell [ref=e173]
              - cell [ref=e175]:
                - button "Review" [ref=e176]
            - row [ref=e179] [cursor=pointer]:
              - cell "#21" [ref=e180]
              - cell "Test Water Leakage in Area 51 Lodged on 7/31/2026" [ref=e181]:
                - generic [ref=e182]: Test Water Leakage in Area 51
                - generic [ref=e183]: Lodged on 7/31/2026
              - cell "Unknown," [ref=e187]:
                - generic "Area 51 Main Street" [ref=e188]: Unknown,
              - cell [ref=e189]
              - cell "8/2/2026 (Normal)" [ref=e191]
              - cell [ref=e193]
              - cell [ref=e195]:
                - button "Review" [ref=e196]
            - row [ref=e199] [cursor=pointer]:
              - cell "#20" [ref=e200]
              - cell "Test Water Leakage in Area 51 Lodged on 7/31/2026" [ref=e201]:
                - generic [ref=e202]: Test Water Leakage in Area 51
                - generic [ref=e203]: Lodged on 7/31/2026
              - cell "Unknown," [ref=e207]:
                - generic "Area 51 Main Street" [ref=e208]: Unknown,
              - cell [ref=e209]
              - cell "8/2/2026 (Normal)" [ref=e211]
              - cell [ref=e213]
              - cell [ref=e215]:
                - button "Review" [ref=e216]
            - row [ref=e219] [cursor=pointer]:
              - cell "#19" [ref=e220]
              - cell "Test Water Leakage in Area 51 Lodged on 7/31/2026" [ref=e221]:
                - generic [ref=e222]: Test Water Leakage in Area 51
                - generic [ref=e223]: Lodged on 7/31/2026
              - cell "Unknown," [ref=e227]:
                - generic "Area 51 Main Street" [ref=e228]: Unknown,
              - cell [ref=e229]
              - cell "8/2/2026 (Normal)" [ref=e231]
              - cell [ref=e233]
              - cell [ref=e235]:
                - button "Review" [ref=e236]
            - row [ref=e239] [cursor=pointer]:
              - cell "#12" [ref=e240]
              - cell "electricity pole damage Lodged on 7/27/2026" [ref=e241]:
                - generic [ref=e242]: electricity pole damage
                - generic [ref=e243]: Lodged on 7/27/2026
              - cell "Phagwara, Punjab" [ref=e247]:
                - generic "Lovely Professional University, NH44, Phagwara, Phagwara Tahsil, Kapurthala, Punjab, 144411, India" [ref=e248]: Phagwara, Punjab
              - cell [ref=e249]
              - cell "7/29/2026 (Normal)" [ref=e251]
              - cell [ref=e253]
              - cell [ref=e255]:
                - button "Review" [ref=e256]
            - row [ref=e259] [cursor=pointer]:
              - cell "#11" [ref=e260]
              - cell "electricity pole Lodged on 7/18/2026" [ref=e261]:
                - generic [ref=e262]: electricity pole
                - generic [ref=e263]: Lodged on 7/18/2026
              - cell "kothagudem, Telangana" [ref=e267]:
                - generic "H.no.4-230" [ref=e268]: kothagudem, Telangana
              - cell [ref=e269]
              - cell "7/20/2026 (Normal)" [ref=e271]
              - cell [ref=e273]
              - cell [ref=e275]:
                - button "Review" [ref=e276]
            - row [ref=e279] [cursor=pointer]:
              - cell "#7" [ref=e280]
              - cell "Test API Lodged on 2/18/2026" [ref=e281]:
                - generic [ref=e282]: Test API
                - generic [ref=e283]: Lodged on 2/18/2026
              - cell "Unknown," [ref=e287]
              - cell [ref=e289]
              - cell "2/20/2026 (Normal)" [ref=e291]
              - cell [ref=e293]
              - cell [ref=e295]:
                - button "Review" [ref=e296]
            - row [ref=e299] [cursor=pointer]:
              - cell "#3" [ref=e300]
              - cell "hiii.. Lodged on 2/16/2026" [ref=e301]:
                - generic [ref=e302]: hiii..
                - generic [ref=e303]: Lodged on 2/16/2026
              - cell "Unknown," [ref=e307]
              - cell [ref=e309]
              - cell "Resolved" [ref=e311]
              - cell [ref=e312]
              - cell [ref=e314]:
                - button "Review" [ref=e315]
            - row [ref=e318] [cursor=pointer]:
              - cell "#2" [ref=e319]
              - cell "hiii.. Lodged on 2/16/2026" [ref=e320]:
                - generic [ref=e321]: hiii..
                - generic [ref=e322]: Lodged on 2/16/2026
              - cell "Unknown," [ref=e326]
              - cell [ref=e328]
              - cell "Resolved" [ref=e330]
              - cell [ref=e331]
              - cell [ref=e333]:
                - button "Review" [ref=e334]
            - row [ref=e337] [cursor=pointer]:
              - cell "#1" [ref=e338]
              - cell "hii... Lodged on 2/16/2026" [ref=e339]:
                - generic [ref=e340]: hii...
                - generic [ref=e341]: Lodged on 2/16/2026
              - cell "Unknown," [ref=e345]
              - cell [ref=e347]
              - cell "Resolved" [ref=e349]
              - cell [ref=e350]
              - cell [ref=e352]:
                - button "Review" [ref=e353]
  - contentinfo [ref=e356]:
    - generic [ref=e359]:
      - generic [ref=e360]:
        - generic [ref=e361]: NyayaSetu
        - paragraph [ref=e362]: Integrated Grievance Redressal and Administrative Monitoring Project. A prototype designed to demonstrate transparent and AI-driven resolution workflows.
      - generic [ref=e363]:
        - generic [ref=e364]: Project Links
        - list [ref=e365]:
          - listitem [ref=e366]:
            - link "National Portal of India" [ref=e367] [cursor=pointer]:
              - /url: https://india.gov.in
          - listitem [ref=e368]:
            - link "Digital India Portal" [ref=e369] [cursor=pointer]:
              - /url: https://digitalindia.gov.in
      - generic [ref=e370]:
        - generic [ref=e371]: Prototype Info
        - paragraph [ref=e372]:
          - text: "For project inquiries or demonstration details:"
          - strong [ref=e373]: "Email:"
          - text: project-nyayasetu@domain.com
          - strong [ref=e374]: "Status:"
          - text: Development Prototype
    - generic [ref=e376]:
      - paragraph [ref=e377]: © 2026 NyayaSetu Project. Developed for demonstration purposes.
      - generic [ref=e378]: Prototype Showcase
```

# Test source

```ts
  20  |   test('Phase 1 & 2: Startup & Landing Page', async () => {
  21  |     // Phase 1: Application Startup
  22  |     const response = await page.goto('/');
  23  |     expect(response?.status()).toBe(200);
  24  | 
  25  |     // Verify no console errors during initial load
  26  |     page.on('console', msg => {
  27  |       if (msg.type() === 'error') {
  28  |         console.error(`Console Error: ${msg.text()}`);
  29  |       }
  30  |     });
  31  | 
  32  |     // Phase 2: Landing Page Checks
  33  |     await expect(page.locator('.brand-title')).toHaveText('NYAYA SETU');
  34  |     await expect(page.getByRole('link', { name: /Login or Register/i }).first()).toBeVisible();
  35  |     
  36  |     // Check navigation links
  37  |     await expect(page.getByRole('link', { name: 'Home', exact: true })).toBeVisible();
  38  |     
  39  |     // Check Theme Toggle
  40  |     const themeBtn = page.locator('.theme-toggle-btn');
  41  |     await themeBtn.click();
  42  |     await themeBtn.click();
  43  |   });
  44  | 
  45  |   test('Phase 3: Login Testing (Negative & Positive)', async () => {
  46  |     await page.getByRole('link', { name: /Login or Register/i }).first().click();
  47  | 
  48  |     // Wait for the form to be ready
  49  |     await expect(page.locator('.login-form-element')).toBeVisible({ timeout: 10000 });
  50  | 
  51  |     // Negative testing
  52  |     await page.locator('#login-username').fill('wronguser');
  53  |     await page.locator('#login-password').fill('wrongpass');
  54  |     await page.getByRole('button', { name: 'Sign In' }).click();
  55  |     try { await expect(page.locator('.login-error-alert')).toBeVisible({ timeout: 2000 }); } catch (e) { console.log(await page.content()); throw e; }
  56  | 
  57  |     // Positive login (Citizen)
  58  |     await page.locator('#login-username').fill('ravi12');
  59  |     await page.locator('#login-password').fill('Charan@24');
  60  |     await page.getByRole('button', { name: 'Sign In' }).click();
  61  | 
  62  |     // Wait for redirect to dashboard
  63  |     await expect(page).toHaveURL(/\/dashboard|\/complaints/);
  64  |   });
  65  | 
  66  |   test('Phase 4: Citizen Dashboard', async () => {
  67  |     await page.getByRole('link', { name: /Dashboard/i }).first().click();
  68  |     await expect(page.getByRole('heading', { name: /Dashboard|Welcome/i })).toBeVisible();
  69  |     await expect(page.locator('.stat-card').first()).toBeVisible();
  70  |   });
  71  | 
  72  |   test('Phase 5: Lodge Complaint', async () => {
  73  |     await page.getByRole('link', { name: /Lodge Grievance/i }).first().click();
  74  |     
  75  |     await expect(page.locator('.lodge-form')).toBeVisible();
  76  | 
  77  |     await page.getByLabel(/Title/i).fill(complaintTitle);
  78  |     await page.getByLabel(/Detailed Explanation/i).fill('There is a massive water pipe burst that needs immediate attention.');
  79  |     
  80  |     const deptSelect = page.locator('#complaint-dept');
  81  |     if (await deptSelect.count() > 0) {
  82  |       await deptSelect.selectOption({ index: 1 });
  83  |     }
  84  |     
  85  |     await page.getByLabel(/Address/i).fill('Area 51 Main Street');
  86  |     
  87  |     await page.getByRole('button', { name: /Submit|Lodge/i }).click();
  88  |     
  89  |     await expect(page).toHaveURL(/\/complaints/);
  90  |     await expect(page.getByText(complaintTitle).first()).toBeVisible();
  91  |   });
  92  | 
  93  |   test('Phase 6: My Complaints', async () => {
  94  |     await page.getByRole('link', { name: /My Complaints|Assigned Grievances/i }).first().click();
  95  |     await expect(page.getByText(complaintTitle).first()).toBeVisible();
  96  |   });
  97  | 
  98  |   test('Phase 7: Logout', async () => {
  99  |     await page.getByRole('link', { name: /Dashboard/i }).first().click();
  100 |     await page.locator('.logout-btn-nav, button[aria-label="Logout"]').click();
  101 |     
  102 |     await expect(page).toHaveURL(/\/$|\/login/);
  103 |     await expect(page.getByRole('link', { name: /Login or Register/i }).first()).toBeVisible();
  104 |   });
  105 | 
  106 |   test('Phase 8 & 9: Officer Login & Dashboard', async () => {
  107 |     await page.getByRole('link', { name: /Login or Register/i }).first().click();
  108 |     
  109 |     await page.locator('#login-username').fill('devansh12');
  110 |     await page.locator('#login-password').fill('Charan@24');
  111 |     await page.getByRole('button', { name: 'Sign In' }).click();
  112 | 
  113 |     await expect(page).toHaveURL(/\/dashboard|\/complaints/);
  114 |     await expect(page.getByText(/Officer Dashboard|Assigned Grievances/i).first()).toBeVisible();
  115 |   });
  116 | 
  117 |   test('Phase 10: Officer Processing', async () => {
  118 |     await page.getByRole('link', { name: /My Complaints|Assigned Grievances/i }).first().click();
  119 |     
> 120 |     await page.getByText(complaintTitle).first().click();
      |                                                  ^ Error: locator.click: Target page, context or browser has been closed
  121 |     await expect(page.locator('.complaint-title-h1')).toHaveText(complaintTitle);
  122 |     
  123 |     const commentInput = page.locator('textarea.comment-textarea-field');
  124 |     if (await commentInput.count() > 0) {
  125 |       await commentInput.fill(officerComment);
  126 |       const sendBtn = page.getByRole('button', { name: /Send/i });
  127 |       if (await sendBtn.count() > 0) {
  128 |         await sendBtn.first().click();
  129 |         await expect(page.getByText(officerComment)).toBeVisible({ timeout: 10000 });
  130 |       }
  131 |     }
  132 | 
  133 |     const resolveBtn = page.getByRole('button', { name: /Mark Resolved/i });
  134 |     if (await resolveBtn.count() > 0) {
  135 |       await resolveBtn.first().click();
  136 |       await expect(page.getByText(/Complaint status updated to 'resolved' successfully!/i)).toBeVisible({ timeout: 10000 });
  137 |     } else {
  138 |       const progressBtn = page.getByRole('button', { name: /Mark In Progress/i });
  139 |       if (await progressBtn.count() > 0) {
  140 |         await progressBtn.first().click();
  141 |         await expect(page.getByText(/Complaint status updated to 'in progress' successfully!/i)).toBeVisible({ timeout: 10000 });
  142 |       }
  143 |     }
  144 |   });
  145 | 
  146 |   test('Phase 11: Citizen Verification', async () => {
  147 |     await page.locator('.logout-btn-nav, button[aria-label="Logout"]').click();
  148 |     
  149 |     await page.getByRole('link', { name: /Login or Register/i }).first().click();
  150 |     await page.locator('#login-username').fill('ravi12');
  151 |     await page.locator('#login-password').fill('Charan@24');
  152 |     await page.getByRole('button', { name: 'Sign In' }).click();
  153 |     
  154 |     await page.getByRole('link', { name: /My Complaints|Assigned Grievances/i }).first().click();
  155 |     await page.getByText(complaintTitle).first().click();
  156 |     
  157 |     await expect(page.getByText(officerComment)).toBeVisible();
  158 |     await expect(page.locator('body')).toContainText(/Resolved/i);
  159 |   });
  160 | });
  161 | 
```