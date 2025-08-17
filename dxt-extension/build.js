#!/usr/bin/env node

/**
 * Build script to package the DXT extension
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createWriteStream } from 'fs';
import archiver from 'archiver';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const outputPath = path.join(__dirname, 'micro-blog-books.dxt');

// Files to include in the extension package
const filesToInclude = [
  'manifest.json',
  'package.json',
  'package-lock.json',
  'server/index.js',
  'icon.svg',
  'README.md',
];

async function buildExtension() {
  console.log('Building DXT extension...');

  // Create output stream
  const output = createWriteStream(outputPath);
  const archive = archiver('zip', {
    zlib: { level: 9 } // Maximum compression
  });

  // Listen for all archive data to be written
  output.on('close', () => {
    console.log(`✓ Extension packaged: ${path.basename(outputPath)}`);
    console.log(`  Total bytes: ${archive.pointer()}`);
    console.log(`  Location: ${outputPath}`);
    console.log('\nTo install:');
    console.log('1. Open Claude Desktop');
    console.log('2. Go to Settings → Extensions');
    console.log('3. Click "Install Extension"');
    console.log(`4. Select: ${outputPath}`);
  });

  // Handle errors
  archive.on('error', (err) => {
    console.error('Error creating archive:', err);
    process.exit(1);
  });

  // Pipe archive data to the file
  archive.pipe(output);

  // Add files to the archive
  for (const file of filesToInclude) {
    const filePath = path.join(__dirname, file);
    
    if (fs.existsSync(filePath)) {
      const stat = fs.statSync(filePath);
      
      if (stat.isFile()) {
        archive.file(filePath, { name: file });
        console.log(`  Added: ${file}`);
      } else if (stat.isDirectory()) {
        archive.directory(filePath, file);
        console.log(`  Added directory: ${file}`);
      }
    } else {
      console.warn(`  Warning: File not found: ${file}`);
    }
  }

  // Add ALL node_modules (including transitive dependencies)
  const nodeModulesPath = path.join(__dirname, 'node_modules');
  if (fs.existsSync(nodeModulesPath)) {
    console.log(`  Adding entire node_modules directory...`);
    archive.directory(nodeModulesPath, 'node_modules');
    console.log(`  ✓ Added all dependencies and transitive dependencies`);
  }

  // Finalize the archive
  await archive.finalize();
}

// Run the build
buildExtension().catch((error) => {
  console.error('Build failed:', error);
  process.exit(1);
});