-- Employees
INSERT INTO employees (name, department, email, password, is_admin) VALUES
('Admin User', 'IT', 'admin@company.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', TRUE), -- password: secret
('John Doe', 'Sales', 'john.doe@company.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', FALSE),
('Jane Smith', 'Marketing', 'jane.smith@company.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', FALSE);

-- Assets
INSERT INTO assets (name, type, serial_number, purchase_date, location, status, owner_id) VALUES
('MacBook Pro 16"', 'Laptop', 'MPB20230001', '2023-01-15', 'Office', 'in_use', 2),
('Canon EOS R5', 'Camera', 'CER20230002', '2023-02-20', 'Studio', 'in_use', 3),
('Dell XPS 15', 'Laptop', 'DXP20220001', '2022-11-10', 'Warehouse', 'decommissioned', NULL),
('Nikon D850', 'Camera', 'ND820230003', '2023-03-05', 'Studio', 'under_maintenance', NULL);

-- Maintenance Records
INSERT INTO maintenance_records (asset_id, maintenance_date, description, cost) VALUES
(4, '2023-06-10', 'Sensor cleaning and calibration', 120.50),
(1, '2023-05-15', 'Battery replacement', 89.99);

-- Asset Allocations
INSERT INTO asset_allocations (asset_id, employee_id, allocation_date, return_date) VALUES
(1, 2, '2023-04-01', NULL),
(2, 3, '2023-04-15', NULL),
(3, 2, '2022-12-01', '2023-03-31');

-- Reservations
INSERT INTO reservations (asset_id, employee_id, reservation_date, start_date, end_date, status) VALUES
(4, 2, '2023-06-01', '2023-07-01', '2023-07-15', 'pending'),
(1, 3, '2023-05-01', '2023-06-01', '2023-06-15', 'approved');