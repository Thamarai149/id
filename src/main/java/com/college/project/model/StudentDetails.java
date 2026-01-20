package com.college.project.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Student Details extracted from ID Card
 * Contains all relevant student information
 */
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class StudentDetails {
    
    private String name;
    private String registerNumber;
    private String rollNumber;
    private String department;
    private String college;
    private String year;
    private String course;
    private String batch;
    private String section;

    public StudentDetails() {}

    public StudentDetails(String name, String registerNumber) {
        this.name = name;
        this.registerNumber = registerNumber;
    }

    // Getters and Setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRegisterNumber() {
        return registerNumber;
    }

    public void setRegisterNumber(String registerNumber) {
        this.registerNumber = registerNumber;
    }

    public String getRollNumber() {
        return rollNumber;
    }

    public void setRollNumber(String rollNumber) {
        this.rollNumber = rollNumber;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getCollege() {
        return college;
    }

    public void setCollege(String college) {
        this.college = college;
    }

    public String getYear() {
        return year;
    }

    public void setYear(String year) {
        this.year = year;
    }

    public String getCourse() {
        return course;
    }

    public void setCourse(String course) {
        this.course = course;
    }

    public String getBatch() {
        return batch;
    }

    public void setBatch(String batch) {
        this.batch = batch;
    }

    public String getSection() {
        return section;
    }

    public void setSection(String section) {
        this.section = section;
    }

    @Override
    public String toString() {
        return "StudentDetails{" +
                "name='" + name + '\'' +
                ", registerNumber='" + registerNumber + '\'' +
                ", department='" + department + '\'' +
                ", college='" + college + '\'' +
                '}';
    }
}