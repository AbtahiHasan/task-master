import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from tasks.models import Employee, Project, Task, TaskDetail


class Command(BaseCommand):
    help = "Seed database with realistic-looking data for Project, Employee, Task, TaskDetail"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true", help="Clear existing data before seeding"
        )

    def handle(self, *args, **options):
        clear = options["clear"]

        # Hardcoded realistic data - no Faker dependency
        projects_data = [
            {"name": "Phytron Website Redesign", "start_date": date(2026, 2, 15)},
            {"name": "Mobile App - TaskMaster", "start_date": date(2026, 3, 1)},
            {"name": "CRM Migration to PostgreSQL", "start_date": date(2026, 1, 20)},
            {"name": "Customer Support Portal", "start_date": date(2026, 4, 10)},
            {"name": "API v2 Development", "start_date": date(2026, 5, 5)},
            {"name": "Marketing Campaign - Summer 2026", "start_date": date(2026, 6, 1)},
        ]

        employees_data = [
            ("Arif Hasan", "arif.hasan@phytron.io"),
            ("Sarah Khan", "sarah.khan@phytron.io"),
            ("John Doe", "john.doe@phytron.io"),
            ("Emily Carter", "emily.carter@phytron.io"),
            ("Rahim Uddin", "rahim.uddin@phytron.io"),
            ("Fatima Ahmed", "fatima.ahmed@phytron.io"),
            ("Michael Brown", "michael.brown@phytron.io"),
            ("Nusrat Jahan", "nusrat.jahan@phytron.io"),
            ("David Smith", "david.smith@phytron.io"),
            ("Aisha Rahman", "aisha.rahman@phytron.io"),
            ("Robert Wilson", "robert.wilson@phytron.io"),
            ("Tania Akter", "tania.akter@phytron.io"),
        ]

        # 25 tasks distributed across projects with realistic titles/descriptions
        # due_date spread: past overdue, near due, future. priority: H/M/L
        tasks_data = [
            {
                "title": "Design landing page mockups",
                "description": "Create high-fidelity mockups for the new Phytron landing page in Figma. Includes hero section, features grid, testimonials, and responsive breakpoints for mobile/tablet. Review with design lead before handoff.",
                "due_date": date(2026, 8, 20),
                "is_completed": True,
                "project_idx": 0,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [0, 3, 5],
            },
            {
                "title": "Implement responsive navigation bar",
                "description": "Build a responsive navbar with Tailwind CSS. Must support dropdown for services, sticky on scroll, and accessible keyboard navigation. Test on Chrome, Safari, and Firefox.",
                "due_date": date(2026, 9, 10),
                "is_completed": True,
                "project_idx": 0,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [1, 6],
            },
            {
                "title": "Optimize image assets and enable lazy loading",
                "description": "Compress all hero images to WebP, implement lazy loading with IntersectionObserver, and add CDN caching headers. Target Lighthouse performance score > 95.",
                "due_date": date(2026, 9, 28),
                "is_completed": False,
                "project_idx": 0,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [2, 6],
            },
            {
                "title": "SEO audit and meta tags implementation",
                "description": "Run Screaming Frog audit, fix missing meta descriptions, add Open Graph and JSON-LD structured data for blog posts. Coordinate with content team for keyword mapping.",
                "due_date": date(2026, 10, 5),
                "is_completed": False,
                "project_idx": 0,
                "priority": TaskDetail.LOW,
                "assignee_indices": [7],
            },
            {
                "title": "Client feedback integration - homepage revisions",
                "description": "Incorporate client feedback from Aug review: adjust color palette to brand guidelines, increase CTA contrast, and rewrite hero copy per marketing input.",
                "due_date": date(2026, 10, 15),
                "is_completed": False,
                "project_idx": 0,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [0, 3],
            },
            # Mobile App - TaskMaster (project 1)
            {
                "title": "Design mobile onboarding flow",
                "description": "UX flow for first-time users: welcome screens, permission requests, and sample task creation. Prototype in Figma and conduct 5 user tests.",
                "due_date": date(2026, 8, 5),
                "is_completed": True,
                "project_idx": 1,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [3, 11],
            },
            {
                "title": "Implement push notification service",
                "description": "Integrate Firebase Cloud Messaging for task reminders and due-date alerts. Handle foreground/background states and deep linking to task detail screen.",
                "due_date": date(2026, 9, 18),
                "is_completed": False,
                "project_idx": 1,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [4, 8, 2],
            },
            {
                "title": "Fix authentication token refresh bug",
                "description": "Users are logged out after 1 hour despite refresh token. Debug Axios interceptor, fix race condition on concurrent requests, add unit tests for auth flow.",
                "due_date": date(2026, 9, 5),
                "is_completed": True,
                "project_idx": 1,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [2, 4],
            },
            {
                "title": "Build offline task sync with SQLite",
                "description": "Enable offline creation/editing of tasks stored locally and sync when online. Use conflict resolution: last-write-wins with server timestamp check.",
                "due_date": date(2026, 10, 20),
                "is_completed": False,
                "project_idx": 1,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [8, 2, 6],
            },
            {
                "title": "App store deployment checklist and screenshots",
                "description": "Prepare App Store and Play Store listings: app icons, 6.5'' and 5.5'' screenshots, privacy policy URL, and release notes for v1.3.0.",
                "due_date": date(2026, 11, 1),
                "is_completed": False,
                "project_idx": 1,
                "priority": TaskDetail.LOW,
                "assignee_indices": [11, 1],
            },
            # CRM Migration (project 2)
            {
                "title": "Analyze legacy CRM data schema",
                "description": "Document MySQL schema from old CRM: 14 tables, 2.3M rows. Identify redundant fields, map to new PostgreSQL normalized schema, and flag PII for encryption.",
                "due_date": date(2026, 7, 15),
                "is_completed": True,
                "project_idx": 2,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [4, 9],
            },
            {
                "title": "Write data migration scripts for PostgreSQL",
                "description": "Python scripts using psycopg2 to migrate batches of 10k rows with transaction and rollback on failure. Log errors to file and validate row counts post-migration.",
                "due_date": date(2026, 8, 30),
                "is_completed": True,
                "project_idx": 2,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [4, 8],
            },
            {
                "title": "Validate migrated customer records",
                "description": "Cross-check 500 random customer records between old and new CRM. Verify email, phone, and purchase history match. Report discrepancies >0.5% to QA.",
                "due_date": date(2026, 9, 12),
                "is_completed": False,
                "project_idx": 2,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [9, 7],
            },
            {
                "title": "Setup nightly backup automation for PostgreSQL",
                "description": "Configure pgBackRest with nightly 2am backups to S3, retention 30 days. Test restore on staging and add Slack alert on failure.",
                "due_date": date(2026, 9, 25),
                "is_completed": False,
                "project_idx": 2,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [8, 10],
            },
            {
                "title": "Train support team on new CRM workflows",
                "description": "Create 3 Loom videos and conduct 2 live workshops for 15 support agents. Cover ticket assignment, new search filters, and reporting dashboard.",
                "due_date": date(2026, 10, 10),
                "is_completed": False,
                "project_idx": 2,
                "priority": TaskDetail.LOW,
                "assignee_indices": [7, 5, 11],
            },
            # Support Portal (project 3)
            {
                "title": "Create ticket submission form with validation",
                "description": "Django form with fields: subject, category, priority, attachment. Server-side validation and rate limiting 5 tickets/hour per user.",
                "due_date": date(2026, 8, 12),
                "is_completed": True,
                "project_idx": 3,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [0, 5],
            },
            {
                "title": "Implement live chat widget integration",
                "description": "Embed Intercom widget, pass authenticated user context, and sync chat transcripts to ticket as internal note. Hide on mobile <375px.",
                "due_date": date(2026, 9, 22),
                "is_completed": False,
                "project_idx": 3,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [6, 1],
            },
            {
                "title": "Design knowledge base article layout",
                "description": "Tailwind layout for KB articles with table of contents, code blocks, and related articles sidebar. Populate with 10 initial articles migrated from Confluence.",
                "due_date": date(2026, 10, 18),
                "is_completed": False,
                "project_idx": 3,
                "priority": TaskDetail.LOW,
                "assignee_indices": [3, 5],
            },
            {
                "title": "Setup role-based access control (RBAC)",
                "description": "Define roles: admin, manager, agent. Agents can only view assigned tickets. Use Django permissions and middleware to enforce at view level. Add tests.",
                "due_date": date(2026, 9, 8),
                "is_completed": True,
                "project_idx": 3,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [2, 4, 10],
            },
            # API v2 (project 4)
            {
                "title": "Design REST API specification v2",
                "description": "OpenAPI 3.0 spec for /api/v2/tasks with pagination, filtering, and sorting. Include error envelope and versioning via Accept header. Review with backend team.",
                "due_date": date(2026, 7, 28),
                "is_completed": True,
                "project_idx": 4,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [2, 8, 10],
            },
            {
                "title": "Implement JWT authentication middleware",
                "description": "Django middleware to verify JWT from Authorization header, handle expiry 15m, refresh via HttpOnly cookie. Add blacklist for logout.",
                "due_date": date(2026, 8, 18),
                "is_completed": True,
                "project_idx": 4,
                "priority": TaskDetail.HIGH,
                "assignee_indices": [2, 4],
            },
            {
                "title": "Optimize dashboard query performance",
                "description": "Reduce N+1 queries on manager dashboard. Use select_related/prefetch_related for Task→Project and TaskDetails. Target query time <150ms for 1k tasks.",
                "due_date": date(2026, 9, 14),
                "is_completed": False,
                "project_idx": 4,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [8, 10],
            },
            {
                "title": "Write API documentation with Swagger",
                "description": "Generate Swagger UI from OpenAPI spec using drf-spectacular. Host at /api/docs/ and include auth examples and Postman collection export.",
                "due_date": date(2026, 10, 2),
                "is_completed": False,
                "project_idx": 4,
                "priority": TaskDetail.LOW,
                "assignee_indices": [9, 1],
            },
            {
                "title": "Setup rate limiting and throttling",
                "description": "DRF throttle: 100 req/min per user, 1000 req/min per IP for anonymous. Return 429 with Retry-After header and log to Prometheus.",
                "due_date": date(2026, 10, 25),
                "is_completed": False,
                "project_idx": 4,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [10, 2],
            },
            # Marketing (project 5)
            {
                "title": "Create summer campaign email templates",
                "description": "3 MJML email templates: launch announcement, weekly digest, win-back. Test rendering on Litmus for Outlook/Gmail/Apple Mail. A/B subject lines.",
                "due_date": date(2026, 9, 30),
                "is_completed": False,
                "project_idx": 5,
                "priority": TaskDetail.MEDIUM,
                "assignee_indices": [1, 7, 11],
            },
            {
                "title": "Analyze Q2 user engagement metrics",
                "description": "Pull Mixpanel data: DAU, retention D7/D30, feature adoption. Build dashboard in Metabase and present insights to marketing lead. Focus on drop-off at onboarding.",
                "due_date": date(2026, 8, 25),
                "is_completed": True,
                "project_idx": 5,
                "priority": TaskDetail.LOW,
                "assignee_indices": [7, 9],
            },
        ]

        with transaction.atomic():
            if clear or Task.objects.exists() or Project.objects.exists() or Employee.objects.exists():
                self.stdout.write(self.style.WARNING("Clearing existing data..."))
                TaskDetail.objects.all().delete()
                Task.objects.all().delete()
                Project.objects.all().delete()
                Employee.objects.all().delete()

            # Create Projects
            projects = []
            for p in projects_data:
                obj = Project.objects.create(name=p["name"], start_date=p["start_date"])
                projects.append(obj)
            self.stdout.write(self.style.SUCCESS(f"Created {len(projects)} projects."))

            # Create Employees
            employees = []
            for name, email in employees_data:
                obj = Employee.objects.create(name=name, email=email)
                employees.append(obj)
            self.stdout.write(self.style.SUCCESS(f"Created {len(employees)} employees."))

            # Create Tasks + M2M + TaskDetail
            created_tasks = 0
            for t in tasks_data:
                project = projects[t["project_idx"]]
                task = Task.objects.create(
                    title=t["title"],
                    description=t["description"],
                    due_date=t["due_date"],
                    is_completed=t["is_completed"],
                    project=project,
                )
                # M2M assigned_to
                assignees = [employees[i] for i in t["assignee_indices"]]
                task.assigned_to.set(assignees)

                # TaskDetail - CharField assigned_to stores primary assignee name
                primary_name = assignees[0].name if assignees else employees[0].name
                TaskDetail.objects.create(
                    task=task,
                    assigned_to=primary_name,
                    priority=t["priority"],
                )
                created_tasks += 1

            self.stdout.write(self.style.SUCCESS(f"Created {created_tasks} tasks with TaskDetails."))

            # Summary
            self.stdout.write(self.style.SUCCESS("Seeding complete:"))
            self.stdout.write(f"  Projects: {Project.objects.count()}")
            self.stdout.write(f"  Employees: {Employee.objects.count()}")
            self.stdout.write(f"  Tasks: {Task.objects.count()}")
            self.stdout.write(f"    - Completed: {Task.objects.filter(is_completed=True).count()}")
            self.stdout.write(f"    - Pending: {Task.objects.filter(is_completed=False).count()}")
            self.stdout.write(f"  TaskDetails: {TaskDetail.objects.count()}")
            self.stdout.write(f"    - High: {TaskDetail.objects.filter(priority='H').count()}")
            self.stdout.write(f"    - Medium: {TaskDetail.objects.filter(priority='M').count()}")
            self.stdout.write(f"    - Low: {TaskDetail.objects.filter(priority='L').count()}")

