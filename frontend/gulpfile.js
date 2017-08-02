'use strict';
var gulp = require('gulp');
var gutil = require('gulp-util');
var watch = require('gulp-watch');





/********
 *  JS  *
 ********/
var uglify = require('gulp-uglify');
gulp.task('scripts', function() {
	return gulp.src('./src/js/*.js')
		.pipe(plumber(function(error) {
			gutil.log(gutil.colors.red(error.message));
			this.emit('end');
		}))
		.pipe(uglify())
		.pipe(gulp.dest('../static/js'));
});

gulp.task('watch-scripts', function() {
    return watch('./src/js/*.js', function() {
        gulp.start('scripts');
    });
});







/********
 * SASS *
 ********/
var plumber = require('gulp-plumber');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var prefix = require('gulp-autoprefixer');

gulp.task('sass', function() {
    return gulp.src('./src/sass/*.scss')
        .pipe(plumber(function(error) {
            gutil.log(gutil.colors.red(error.message));
            this.emit('end');
        }))
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(sourcemaps.write())
        .pipe(prefix({browsers: ['last 2 version']}))
        .pipe(gulp.dest('../static/css'));
});

gulp.task('watch-sass', function() {
    return watch('./src/sass/**/*.scss', function() {
        gulp.start('sass');
    });
});





/********
 * COPY *
 ********/
gulp.task('copy-images', function() {
    return gulp.src('./src/images/**/*', {base: './src/images'})
        .pipe(gulp.dest('../static/img/'));
});
gulp.task('watch-copy-images', function() {
    return watch('./src/images/**/*', function() {
        gulp.start('copy-images');
    });
});
gulp.task('copy-fonts', function() {
    return gulp.src('./src/fonts/**/*', {base: './src/fonts'})
        .pipe(gulp.dest('../static/fonts/'));
});
gulp.task('watch-copy-fonts', function() {
    return watch('./src/fonts/**/*', function() {
        gulp.start('copy-fonts');
    });
});

gulp.task('copy', ['copy-images', 'copy-images']);
gulp.task('watch-copy', ['watch-copy-images', 'copy-fonts']);





/***************
 * COLLECTIONS *
 ***************/
gulp.task('build', ['sass', 'scripts', 'copy']);
gulp.task('watch', ['build'], function() {
    gulp.start(['watch-sass', 'watch-copy', 'watch-scripts']);
});

gulp.task('default', ['watch']);
