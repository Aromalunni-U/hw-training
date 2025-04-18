use("companyDB");

db.employees.insertOne({
    empId: 101,
    name: "Ravi",
    department: "IT",
    salary: 75000,
    isActive: true
});

db.employees.insertMany([
  {
    empId: 102,
    name: "Abhi",
    department: "IT",
    salary: 50000,
    isActive: true
  },
  {
    empId: 103,
    name: "Kavi",
    department: "IT",
    salary: 35000,
    isActive: false
  },
  {
    empId: 104,
    name: "Levi",
    department: "Sales",
    salary: 75000,
    isActive: true
  },
  {
    empId: 105,
    name: "Goku",
    department: "IT",
    salary: 55000,
    isActive: false
  },
  {
    empId: 106,
    name: "Naruto",
    department: "Sales",
    salary: 60000,
    isActive: true
  }
]);

db.employees.updateMany({ department: "IT" },{ $mul: { salary: 1.1 } });

db.employees.deleteMany({ isActive: false });
